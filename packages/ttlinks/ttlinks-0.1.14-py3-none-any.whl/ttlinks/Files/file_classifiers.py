import os
from abc import abstractmethod
from enum import Enum

from ttlinks.common.base_utils import CoRHandler

class FileType(Enum):
    UNKNOWN = 0
    TXT = 1
    CSV = 2

class FileClassifierHandler(CoRHandler):
    _next_handler = None

    def set_next(self, h: CoRHandler) -> CoRHandler:
        if not isinstance(h, CoRHandler):
            raise TypeError("The next handler must be an instance of CoRHandler.")
        self._next_handler = h
        return h

    @abstractmethod
    def handle(self, file_path: str):
        if self._next_handler:
            return self._next_handler.handle(file_path)
        return FileType.UNKNOWN


class TxtFileClassifierHandler(FileClassifierHandler):
    def handle(self, file_path: str):
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.txt':
            return FileType.TXT
        else:
            return super().handle(file_path)


class CsvFileClassifierHandler(FileClassifierHandler):
    def handle(self, file_path: str):
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.csv':
            return FileType.CSV
        else:
            return super().handle(file_path)


class FileClassifier:
    @staticmethod
    def classify_files(file_path: str):
        classifiers = [
            TxtFileClassifierHandler(),
            CsvFileClassifierHandler(),
        ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(file_path)

