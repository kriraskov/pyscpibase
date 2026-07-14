from adapters.adapter import Adapter
from typing import Self, Sequence


class FakeAdapter(Adapter):
    _buffer = ""

    def open(self) -> Self:
        return self

    def close(self) -> None:
        pass

    def read(self) -> str:
        message = self._buffer
        self._buffer = ""
        return message

    def read_binary_values(self) -> Sequence[int | float]:
        raise NotImplementedError()

    def write(self, message: str) -> None:
        self._buffer += message + ";"

    def write_binary_values(
            self,
            message: str,
            values: Sequence[int | float]
    ) -> None:
        raise NotImplementedError()
