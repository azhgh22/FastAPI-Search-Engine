from typing import Protocol

class FileReaderI(Protocol):
    def read(self) -> list[dict]:
        pass