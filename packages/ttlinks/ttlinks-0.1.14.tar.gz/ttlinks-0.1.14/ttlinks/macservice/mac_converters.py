from __future__ import annotations

import re
from abc import abstractmethod
from typing import Any, List

from ttlinks.common.base_utils import CoRHandler, BinaryClass, BinaryFlyWeightFactory
from ttlinks.common.tools import NumeralConverter
from ttlinks.ipservice.ip_address import IPv6Addr


class MACConverterHandler(CoRHandler):
    _next_handler = None

    def __init__(self, padding: bool = True):
        self._padding = padding  # padding 0 from left to right to fill total of 48

    def set_padding(self, padding: bool):
        self._padding = padding

    def set_next(self, h: CoRHandler) -> CoRHandler:
        if not isinstance(h, CoRHandler):
            raise TypeError("The next handler must be an instance of CoRHandler.")
        self._next_handler = h
        return h

    @abstractmethod
    def handle(self, request: Any):
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Abstract method to be implemented in derived classes to convert the request into a list of BinaryClass instances.

        Parameters:
            request (Any): The request to be converted.

        Returns:
            List[BinaryClass]: A list of BinaryClass instances representing the request.
        """
        pass


class BinaryClassMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if len(request) == 6:
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: List[BinaryClass]) -> List[BinaryClass]:
        return request


class BinaryDigitsMAC48ConverterHandler(MACConverterHandler):
    """
    Handles the binary conversion of MAC-48 addresses. This class extends MACConverterHandler
    to specifically convert 48-bit integer lists into BinaryClass instances.
    """

    def handle(self, request: Any):
        """
        Handles conversion of a list of integers representing a 48-bit MAC address into binary format.
        If the request is not a valid 48 integer list, it passes the request up the chain.

        Parameters:
            request (Any): A list of integers representing a MAC address.

        Returns:
            Processes the request if valid; otherwise, returns the result of the superclass handle method.
        """
        if isinstance(request, list) and all(isinstance(item, int) for item in request) and len(request) == 48:
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Converts a 48-element integer list (representing a MAC address) into a list of BinaryClass objects.

        Parameters:
            request (Any): A list of integers representing a MAC address.

        Returns:
            List[BinaryClass]: A list of BinaryClass objects created from the binary representation of each byte.
        """
        binary_string_list = [
            ''.join(map(str, request[bit_index: bit_index + 8]))
            for bit_index in range(0, len(request), 8)
        ]
        return [
            BinaryFlyWeightFactory.get_binary_class(binary_string)
            for binary_string in binary_string_list
        ]


class DashedHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace('-', '').upper()):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        raw_mac = request.replace('-', '').upper()
        return [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]


class ColonHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace(':', '').upper()):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        raw_mac = request.replace(':', '').upper()
        return [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]


class DotHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace('.', '').upper()):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        raw_mac = request.replace('.', '').upper()
        return [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]


class BinaryClassOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if len(request) == 3:
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: List[BinaryClass]) -> List[BinaryClass]:
        return request


class BinaryDigitsOUI24ConverterHandler(MACConverterHandler):

    def handle(self, request: Any):
        if isinstance(request, list) and all(isinstance(item, int) for item in request) and len(request) == 24:
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        binary_string_list = [
            ''.join(map(str, request[bit_index: bit_index + 8]))
            for bit_index in range(0, len(request), 8)
        ]
        result = [BinaryFlyWeightFactory.get_binary_class(binary_string) for binary_string in binary_string_list]
        if self._padding:
            result.extend([BinaryFlyWeightFactory.get_binary_class('00000000')] * 3)
        return result


class DashedHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace('-', '').upper()):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        raw_mac = request.replace('-', '').upper()
        result = [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]
        if self._padding:
            result.extend([BinaryFlyWeightFactory.get_binary_class('00000000')] * 3)
        return result


class ColonHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace(':', '').upper()):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        raw_mac = request.replace(':', '').upper()
        result = [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]
        if self._padding:
            result.extend([BinaryFlyWeightFactory.get_binary_class('00000000')] * 3)
        return result


class DotHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace('.', '').upper()):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        raw_mac = request.replace('.', '').upper()
        result = [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]
        if self._padding:
            result.extend([BinaryFlyWeightFactory.get_binary_class('00000000')] * 3)
        return result


class BinaryClassEUI64ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if len(request) == 6:
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: List[BinaryClass]) -> List[BinaryClass]:
        left_binary_digits = [octet.binary_digits for octet in request[0:3]]
        right_binary_digits = [octet.binary_digits for octet in request[3:]]
        middle = [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(hexadecimal)).binary_digits
            for hexadecimal in ['ff', 'fe']
        ]
        left_binary_digits[0][6] = 1 if int(left_binary_digits[0][6]) == 0 else 0
        eui64_binary_digits = left_binary_digits + middle + right_binary_digits
        return [
            BinaryFlyWeightFactory.get_binary_class(''.join(map(str, binary_digit)))
            for binary_digit in eui64_binary_digits
        ]


class MACConverter:
    @staticmethod
    def convert_mac(mac: Any, converters: List[MACConverterHandler] = None) -> List[BinaryClass]:
        if converters is None:
            converters = [
                BinaryClassMAC48ConverterHandler(),
                BinaryDigitsMAC48ConverterHandler(),
                DashedHexMAC48ConverterHandler(),
                ColonHexMAC48ConverterHandler(),
                DotHexMAC48ConverterHandler()
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(mac)

    @staticmethod
    def convert_oui(mac: Any, converters: List[MACConverterHandler] = None) -> List[BinaryClass]:
        if converters is None:
            converters = [
                BinaryClassMAC48ConverterHandler(),
                BinaryDigitsMAC48ConverterHandler(),
                DashedHexMAC48ConverterHandler(),
                ColonHexMAC48ConverterHandler(),
                DotHexMAC48ConverterHandler(),
                BinaryClassOUI24ConverterHandler(),
                BinaryDigitsOUI24ConverterHandler(),
                DashedHexOUI24ConverterHandler(),
                ColonHexOUI24ConverterHandler(),
                DotHexOUI24ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(mac)

    @staticmethod
    def convert_to_eui64(mac: Any) -> List[BinaryClass]:
        mac_address = MACConverter.convert_mac(mac)
        converter_handler = BinaryClassEUI64ConverterHandler()
        return converter_handler.handle(mac_address)
