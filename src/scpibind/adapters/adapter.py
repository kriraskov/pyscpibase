from abc import ABC, abstractmethod
from typing import Self, Sequence
import time


class Adapter(ABC):
    @abstractmethod
    def open(self) -> Self:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def read(self) -> str:
        ...

    @abstractmethod
    def read_binary_values(self) -> Sequence[float]:
        ...

    @abstractmethod
    def write(self, message: str) -> None:
        ...

    @abstractmethod
    def write_binary_values(
            self,
            message: str,
            values: Sequence[float]
    ) -> None:
        ...

    def query(self, message: str, delay: float | None = None) -> str:
        self.write(message)
        if delay is not None:
            time.sleep(delay)
        return self.read()

    def query_binary_values(
            self,
            message: str,
            delay: float | None = None
    ) -> Sequence[float]:
        self.write(message)
        if delay is not None:
            time.sleep(delay)
        return self.read_binary_values()
