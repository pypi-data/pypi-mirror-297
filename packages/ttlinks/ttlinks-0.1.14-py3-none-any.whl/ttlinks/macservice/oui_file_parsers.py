import copy
import hashlib
import os
import re
from abc import abstractmethod, ABC
from typing import List, Dict, Union

from ttlinks.Files.file_classifiers import FileType
from ttlinks.Files.file_utils import File
from ttlinks.common.base_utils import CoRHandler, BinaryClass, BinaryFlyWeightFactory
from ttlinks.common.tools import NumeralConverter
from ttlinks.macservice.mac_converters import BinaryDigitsMAC48ConverterHandler
from ttlinks.macservice.oui_utils import OUIType, OUIUnit

class IEEEOuiFile(File):
    """
    A concrete implementation of the File abstract class, specifically designed to handle IEEE OUI (Organizationally
    Unique Identifier) files. This class reads the content of an IEEE OUI file and makes it available through the
    file_content property.

    The IEEEOuiFile class is typically used to pass along OUI file content to parsers and other processes that
    handle such data, allowing for dynamic changes to the properties as necessary during runtime.
    """

    def _validate(self):
        super()._validate()

    def _read(self):
        """
        Reads the contents of the OUI file specified by the file path using the method specified by _read_method.
        The content is stored in the _file_content attribute, making it accessible via the file_content property.
        """
        self._file_content = open(self._file_path, self._read_method).read()


class OUIFileParserHandler(CoRHandler):
    """
    Abstract base handler in a Chain of Responsibility pattern designed for parsing IEEE OUI files.
    It supports original .txt and .csv files downloaded from the IEEE registration authority without modification.
    OUI download link https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries
    The class can handle various OUI types like IAB, MA-S, MA-M, CID, and MA-L.

    Attributes:
        _next_handler (CoRHandler): Reference to the next handler in the chain.
        _previous_handler (CoRHandler): Reference to the previous handler in the chain.
        _file (IEEEOuiFile): The file being processed.

    Methods:
        set_next: Sets the next handler in the chain and links back to this handler as previous.
        _generate_file_information: Opens or reuses the file based on chain position.
        parse: Abstract method to parse the OUI document.
        handle: Passes the document path to the next handler if available.
        _parse_mac_range: Abstract method to parse MAC range from binary class representations.
        _parse_physical_address: Abstract method to parse physical addresses.
    """
    _next_handler = None
    _previous_handler = None
    _file = None

    @abstractmethod
    def __init__(self):
        self._mask: List[BinaryClass] = []
        self._oui_type: OUIType = OUIType.UNKNOWN

    @property
    def file(self):
        """Provides access to the currently processed file."""
        return self._file

    def set_next(self, h: CoRHandler) -> CoRHandler:
        """
        Sets the next handler in the responsibility chain and establishes a bidirectional link between handlers.

        Parameters:
            h (CoRHandler): The next handler in the chain.

        Returns:
            CoRHandler: The handler set as next.
        """
        if not isinstance(h, CoRHandler):
            raise TypeError("The next handler must be an instance of CoRHandler.")
        self._next_handler = h
        h._previous_handler = self
        return h

    def _generate_file_information(self, oui_doc_path: str):
        """
        Opens or reuses the file depending on whether it was already opened by a previous handler.

        Parameters:
            oui_doc_path (str): Path to the OUI document.
        """
        if self._previous_handler and self._previous_handler.file:
            self._file = self._previous_handler.file
        else:
            self._file = IEEEOuiFile(oui_doc_path)

    @abstractmethod
    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """Abstract method to parse the document and extract OUI information."""
        pass

    @abstractmethod
    def handle(self, oui_doc_path: str):
        """
        Processes or passes the OUI document path along the chain.

        Parameters:
            oui_doc_path (str): Path to the OUI document.
        """
        if self._next_handler:
            return self._next_handler.handle(oui_doc_path)
        return self._next_handler

    @abstractmethod
    def _parse_mac_range(self, mac: List[BinaryClass], oui_mask: List[BinaryClass]) -> List[str]:
        """Abstract method to calculate and parse the MAC range from binary representations."""
        pass

    @abstractmethod
    def _parse_physical_address(self, *args: str) -> str:
        """Abstract method to format and clean up physical address strings."""
        pass


class OUITxtFileParserHandler(OUIFileParserHandler, ABC):
    """
    A concrete handler in the Chain of Responsibility pattern specifically designed to parse IEEE OUI information
    from .txt files. It implements abstract methods from OUIFileParserHandler to handle and process OUI data
    effectively, adjusting for the specific format and nuances of .txt documents.

    Inherits:
        OUIFileParserHandler: Inherits basic handler functionalities and abstract methods for OUI parsing.
    """

    def _parse_mac_range(self, mac: List[BinaryClass], oui_mask: List[BinaryClass]) -> List[str]:
        """
        Parses the MAC address range based on given MAC addresses and masks. This involves converting
        binary MAC addresses into their hexadecimal representations, adjusting for any masking applied
        to determine the range of addresses covered by the OUI.

        Parameters:
            mac (List[BinaryClass]): List of BinaryClass instances representing the MAC address.
            oui_mask (List[BinaryClass]): List of BinaryClass instances representing the mask applied to the MAC address.

        Returns:
            List[str]: A list containing the start and end MAC addresses in the hexadecimal format.
        """
        original_mac_binary_digits = []
        mask_binary_digits = []
        for mac_octet in mac:
            original_mac_binary_digits += mac_octet.binary_digits
        for mask_octet in oui_mask:
            mask_binary_digits += mask_octet.binary_digits
        non_matching_indices = mask_binary_digits.count(0)
        after_matching_mac_binary_digits = copy.deepcopy(original_mac_binary_digits)
        after_matching_mac_binary_digits[-non_matching_indices:] = ([1] * (non_matching_indices - 1)) + [1]
        binary_digits_mac48_converter = BinaryDigitsMAC48ConverterHandler()
        return [
            ':'.join(NumeralConverter.binary_to_hexadecimal(str(mac_binary)).rjust(2, '0')
                     for mac_binary in binary_digits_mac48_converter.handle(original_mac_binary_digits)),
            ':'.join(NumeralConverter.binary_to_hexadecimal(str(mac_binary)).rjust(2, '0')
                     for mac_binary in binary_digits_mac48_converter.handle(after_matching_mac_binary_digits)),
        ]

    def _parse_physical_address(self, address_line1: str, address_line2: str, country: str) -> str:
        """
        Formats and cleans up the physical address from components typically found in OUI .txt files.
        It combines different parts of the address and ensures a standard formatting is applied,
        removing excess whitespace and other common formatting issues.

        Parameters:
            address_line1 (str): The primary line of the address.
            address_line2 (str): The secondary line of the address, which may contain additional details like city and state.
            country (str): The country where the organization is located.

        Returns:
            str: A formatted string that represents the full physical address.
        """
        if address_line1 == '':  # skip if there is no address. meaning a private OUI range
            return ''
        full_address = f"{address_line1}, "
        address_line2_component = re.split(r'\s{2,}', address_line2)
        if len(address_line2_component) == 2:
            full_address += ' '.join(address_line2_component)
        if len(address_line2_component) == 3:
            full_address += f"{address_line2_component[0]}, "
            full_address += ' '.join(address_line2_component[1:])
        full_address += f", {country}"
        return full_address.replace('  ', ' ').replace('"', '').replace(',,', ',').strip()


class OUICsvFileParserHandler(OUIFileParserHandler, ABC):
    """
    A concrete handler in the Chain of Responsibility pattern specifically tailored for parsing IEEE OUI information
    from .csv files. This class extends the OUIFileParserHandler to specifically handle the parsing of .csv formatted
    OUI data, applying the necessary logic to interpret and process CSV-specific data structuring.

    Inherits:
        OUIFileParserHandler: Inherits basic handler functionalities and abstract methods for parsing OUI data.
    """

    def _parse_mac_range(self, mac: List[BinaryClass], oui_mask: List[BinaryClass]) -> List[str]:
        """
        Parses the MAC address range based on the provided MAC addresses and their corresponding masks. This method
        calculates the start and end MAC addresses by interpreting binary representations of MAC addresses, adjusting them
        based on the mask to determine the full range of MAC addresses that the OUI could potentially cover.

        Parameters:
            mac (List[BinaryClass]): List of BinaryClass instances representing the original MAC address.
            oui_mask (List[BinaryClass]): List of BinaryClass instances representing the mask applied to the MAC address.

        Returns:
            List[str]: A list containing two strings representing the start and end MAC addresses in hexadecimal format.
        """
        original_mac_binary_digits = []
        mask_binary_digits = []
        for mac_octet in mac:
            original_mac_binary_digits += mac_octet.binary_digits
        for mask_octet in oui_mask:
            mask_binary_digits += mask_octet.binary_digits
        non_matching_indices = mask_binary_digits.count(0)
        after_matching_mac_binary_digits = copy.deepcopy(original_mac_binary_digits)
        after_matching_mac_binary_digits[-non_matching_indices:] = ([1] * (non_matching_indices - 1)) + [1]
        binary_digits_mac48_converter = BinaryDigitsMAC48ConverterHandler()
        return [
            ':'.join(NumeralConverter.binary_to_hexadecimal(str(mac_binary)).rjust(2, '0')
                     for mac_binary in binary_digits_mac48_converter.handle(original_mac_binary_digits)),
            ':'.join(NumeralConverter.binary_to_hexadecimal(str(mac_binary)).rjust(2, '0')
                     for mac_binary in binary_digits_mac48_converter.handle(after_matching_mac_binary_digits)),
        ]

    def _parse_physical_address(self, address_line: str) -> str:
        """
        Cleans up and formats the physical address extracted from a .csv file. This method focuses on removing
        unnecessary characters and spaces, ensuring that the address is presented in a clean and uniform format.

        Parameters:
            address_line (str): The complete address line extracted from the CSV file.

        Returns:
            str: A formatted string representing the cleaned-up physical address.
        """
        return address_line.replace('  ', ' ').replace('"', '').replace(',,', ',').strip()


class IabOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    A specialized handler for parsing IEEE IAB OUI information from text files. This handler is configured to
    specifically detect and parse OUI data formatted for IAB ranges, which includes custom mask settings and specific
    patterns in the text content.

    Inherits:
        OUITxtFileParserHandler: Inherits text file parsing capabilities with adaptations for IAB specific format.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask and OUI type settings for IAB records. The mask is defined to
        accommodate the specific structure of IAB entries in the OUI data files.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))]
        )
        self._oui_type = OUIType.IAB

    def handle(self, oui_doc_path: str):
        """
        Handles the parsing of an OUI document located at the specified path, tailored for IAB entries.
        This method checks the file content for specific markers indicating IAB data and delegates to the parse method
        if appropriate.

        Parameters:
            oui_doc_path (str): Path to the OUI document.

        Returns:
            Dict[str, List[OUIUnit]] or passes handling to the next handler if IAB specific content is not found.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'IAB Range\s+Organization', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the OUI document for IAB-specific entries and extracts detailed information into structured OUI units.

        Parameters:
            oui_doc (str): The content of the OUI document.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed OUI units along with the MD5 hash of the document
            for integrity and tracking purposes.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6}-\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = mac_range[:mac_range.find('-')]
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class MasOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    Handles the parsing of MA-S OUI data from text files. This handler looks for specific markers that identify
    MA-S ranges in the file and processes them accordingly.

    Inherits:
        OUITxtFileParserHandler: Inherits the general text file parsing methods with custom behavior for MA-S OUI entries.
    """
    def __init__(self):
        """
        Sets up the mask and OUI type specifically for MA-S entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))]
        )
        self._oui_type = OUIType.MA_S

    def handle(self, oui_doc_path: str):
        """
        Checks the file content for MA-S specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'OUI-36/MA-S Range\s+Organization', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the OUI document content and extracts detailed OUI units, storing them along with an MD5 hash of the content
        for verification and reference purposes.

        Parameters:
            oui_doc (str): The content of the OUI document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6}-\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = mac_range[:mac_range.find('-')]
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class MamOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    Handles the parsing of MA-M OUI data from text files. This handler is specifically configured to detect and
    process entries for MA-M ranges, adjusting the mask settings appropriately for this OUI type.

    Inherits:
        OUITxtFileParserHandler: Inherits text file parsing capabilities with adaptations for MA-M OUI entries.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask settings and OUI type for MA-M entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))] * 2
        )
        self._oui_type = OUIType.MA_M

    def handle(self, oui_doc_path: str):
        """
        Checks the file content for MA-M specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'OUI-28/MA-M Range\s+Organization', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Extracts detailed OUI units from the document, specifically targeting MA-M ranges, and stores them along with an MD5 hash
        of the content for verification purposes.

        Parameters:
            oui_doc (str): The content of the OUI document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6}-\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = mac_range[:mac_range.find('-')]
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class MalOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    Handles the parsing of MA-L OUI data from text files. This handler is specifically configured to detect and
    process entries for MA-L ranges, adapting the mask settings appropriately for MA-L type OUIs.

    Inherits:
        OUITxtFileParserHandler: Inherits text file parsing capabilities with adaptations for MA-L OUI entries.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask settings and OUI type for MA-L entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))] * 3
        )
        self._oui_type = OUIType.MA_L

    def handle(self, oui_doc_path: str):
        """
        Checks the file content for MA-L specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'OUI/MA-L\s+Organization', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Extracts detailed OUI units from the document, specifically targeting MA-L ranges, and stores them along with an MD5 hash
        of the content for verification purposes.

        Parameters:
            oui_doc (str): The content of the OUI document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = '000000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class CidOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    Handles the parsing of CID (Company ID) OUI data from text files. This handler specifically configures
    itself to detect and process CID entries, applying a mask that's appropriate for CID type OUIs.

    Inherits:
        OUITxtFileParserHandler: Inherits general text file parsing methods with specific behavior for CID OUI entries.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask settings and OUI type for CID entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))] * 3
        )
        self._oui_type = OUIType.CID

    def handle(self, oui_doc_path: str):
        """
        Checks the file content for CID specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'CID\s+Organization', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the OUI document for CID entries and extracts detailed information into structured OUI units,
        storing them along with an MD5 hash of the content for verification and reference purposes.

        Parameters:
            oui_doc (str): The content of the OUI document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = '000000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class IabOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles the parsing of IAB OUI data from CSV files. This handler specifically configures itself to detect and
    process IAB entries in CSV format, applying a specific mask that’s appropriate for IAB type OUIs.

    Inherits:
        OUICsvFileParserHandler: Inherits CSV file parsing capabilities with specific adaptations for IAB OUI entries.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask settings and OUI type for IAB entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))]
        )
        self._oui_type = OUIType.IAB

    def handle(self, oui_doc_path: str):
        """
        Checks the CSV file content for IAB specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the CSV document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'IAB,[0-9A-F]{9}', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the CSV document for IAB entries and extracts detailed information into structured OUI units,
        storing them along with an MD5 hash of the content for verification and reference purposes.

        Parameters:
            oui_doc (str): The content of the CSV document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'IAB,([0-9A-F]{6})([0-9A-F]{3}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, range_octets, company, address_line = match
                oui_hex = oui_hex.strip()
                range_octets = range_octets.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = range_octets.strip() + '000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))
        return result


class MasOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles the parsing of MA-S OUI data from CSV files. This handler is specifically configured to detect and
    process MA-S entries, applying a mask that’s tailored for MA-S type OUIs.

    Inherits:
        OUICsvFileParserHandler: Inherits CSV file parsing capabilities with specific adaptations for MA-S OUI entries.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask settings and OUI type for MA-S entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))]
        )
        self._oui_type = OUIType.MA_S

    def handle(self, oui_doc_path: str):
        """
        Checks the CSV file content for MA-S specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the CSV document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'MA-S,[0-9A-F]{9}', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the CSV document for MA-S entries and extracts detailed information into structured OUI units,
        storing them along with an MD5 hash of the content for verification and reference purposes.

        Parameters:
            oui_doc (str): The content of the CSV document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'MA-M,([0-9A-F]{6})([0-9A-F]{3}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, range_octets, company, address_line = match
                oui_hex = oui_hex.strip()
                range_octets = range_octets.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = range_octets.strip() + '000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))
        return result


class MamOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles the parsing of MA-M OUI data from CSV files. This handler is specifically configured to detect and
    process MA-M entries, applying a tailored mask for this type of OUI.

    Inherits:
        OUICsvFileParserHandler: Inherits CSV file parsing capabilities with specific adaptations for MA-M OUI entries.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask settings and OUI type for MA-M entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))] * 2
        )
        self._oui_type = OUIType.MA_M

    def handle(self, oui_doc_path: str):
        """
        Checks the CSV file content for MA-M specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the CSV document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'MA-M,[0-9A-F]{7}', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the CSV document for MA-M entries and extracts detailed information into structured OUI units,
        storing them along with an MD5 hash of the content for verification and reference purposes.

        Parameters:
            oui_doc (str): The content of the CSV document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'MA-M,([0-9A-F]{6})([0-9A-F]{1}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, range_octets, company, address_line = match
                oui_hex = oui_hex.strip()
                range_octets = range_octets.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = range_octets.strip() + '00000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))
        return result


class MalOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles the parsing of MA-L OUI data from CSV files. This handler is specifically configured to detect and
    process MA-L entries, applying a tailored mask for this type of OUI.

    Inherits:
        OUICsvFileParserHandler: Inherits CSV file parsing capabilities with specific adaptations for MA-L OUI entries.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask settings and OUI type for MA-L entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))] * 3
        )
        self._oui_type = OUIType.MA_L

    def handle(self, oui_doc_path: str):
        """
        Checks the CSV file content for MA-L specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the CSV document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'MA-L,[0-9A-F]{6}', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the CSV document for MA-L entries and extracts detailed information into structured OUI units,
        storing them along with an MD5 hash of the content for verification and reference purposes.

        Parameters:
            oui_doc (str): The content of the CSV document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'MA-L,([0-9A-F]{6}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company, address_line = match
                oui_hex = oui_hex.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = '000000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))

        return result


class CidOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles the parsing of CID (Company ID) OUI data from CSV files. This handler specifically configures itself to detect and
    process CID entries in CSV format, applying a specific mask that’s appropriate for CID type OUIs.

    Inherits:
        OUICsvFileParserHandler: Inherits CSV file parsing capabilities with specific adaptations for CID OUI entries.
    """
    def __init__(self):
        """
        Initializes the handler with specific mask settings and OUI type for CID entries.
        """
        self._mask: List[BinaryClass] = (
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary('00'))] * 3
        )
        self._oui_type = OUIType.CID

    def handle(self, oui_doc_path: str):
        """
        Checks the CSV file content for CID specific content and delegates parsing if found, otherwise passes handling up the chain.

        Parameters:
            oui_doc_path (str): Path to the CSV document to be processed.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'CID,[0-9A-F]{6}', self._file.file_content):
            return self.parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the CSV document for CID entries and extracts detailed information into structured OUI units,
        storing them along with an MD5 hash of the content for verification and reference purposes.

        Parameters:
            oui_doc (str): The content of the CSV document.

        Returns:
            Dict[str, List[OUIUnit]]: Contains the MD5 hash of the document and a list of parsed OUI units.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'CID,([0-9A-F]{6}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company, address_line = match
                oui_hex = oui_hex.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = '000000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [BinaryFlyWeightFactory.get_binary_class(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))
        return result


class OuiFileParser:
    """
    A parser class designed to facilitate the parsing of OUI files, supporting both .csv and .txt file formats.
    It uses a chain of responsibility pattern to delegate the parsing task to the appropriate handler based on the
    file type and content. The handlers are arranged to prioritize smaller OUI ranges first, ensuring that the masks
    are applied in the most specific order possible.

    Methods:
        parse_oui_file: Static method to parse the OUI file based on its extension and delegate to the correct parser handler.
    """
    @staticmethod
    def parse_oui_file(oui_file_path: str, parsers: List[OUIFileParserHandler] = None, to_json: bool = True) -> Union[Dict, None]:
        """
        Parses the OUI file at the given path using an appropriate handler based on the file extension and the list of parser handlers provided.
        The parsing handlers are configured to check for smaller OUI ranges first, ensuring specificity in mask application.

        Parameters:
            oui_file_path (str): The file path of the OUI file to be parsed.
            parsers (list): A list of initialized parser handler objects that will be used to attempt parsing the OUI file.
                            This list should be ordered from the most specific to the least specific handler in terms of the OUI range size they handle.

        Returns:
            Dict or None: Returns the parsing result if successful; otherwise, passes through exceptions for unsupported formats.

        Raises:
            ValueError: If the file extension is neither .csv nor .txt, indicating unsupported file format.
        """
        _, ext = os.path.splitext(oui_file_path)
        if ext.lower() not in ['.csv', '.txt']:
            raise ValueError(f"Only .csv and .txt files are supported by OUI file parsers.")
        if parsers is None:
            parsers = [
                IabOuiTxtFileParserHandler(),
                IabOuiCsvFileParserHandler(),
                MasOuiTxtFileParserHandler(),
                MasOuiCsvFileParserHandler(),
                MamOuiTxtFileParserHandler(),
                MamOuiCsvFileParserHandler(),
                MalOuiTxtFileParserHandler(),
                MalOuiCsvFileParserHandler(),
                CidOuiTxtFileParserHandler(),
                CidOuiCsvFileParserHandler(),
            ]
        parser_handler = parsers[0]
        for next_handler in parsers[1:]:
            parser_handler.set_next(next_handler)
            parser_handler = next_handler
        return parsers[0].handle(oui_file_path)
