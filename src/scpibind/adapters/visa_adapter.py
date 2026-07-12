from adapter import Adapter
from pyvisa import ResourceManager
from typing import Self, Sequence, Any


class VISAAdapter(Adapter):
    def __init__(self, resource_name: str, rm: ResourceManager | None = None,
                 **resource_kwargs) -> None:
        self.resource_name = resource_name
        self.rm = rm or ResourceManager()
        self.resource_kwargs = resource_kwargs
        self._resource = None

    def open(self) -> Self:
        if self._resource is None:
            self._resource = self.rm.open_resource(
                self.resource_name,
                **self.resource_kwargs
            )
        return self

    def close(self):
        if self._resource is not None:
            self._resource.close()
            self._resource = None

    def read(self) -> str:
        return self._resource.read()

    def read_binary_values(self) -> Sequence[int | float]:
        return self._resource.read_binary_values()

    def write(self, message: str) -> None:
        self._resource.write(message)

    def write_binary_values(
            self,
            message: str,
            values: Sequence[int | float]
    ) -> None:
        self._resource.write_binary_values(message, values)

    def query(self, message: str, delay: int | float | None = None) -> None:
        return self._resource.query(message, delay)

    def query_binary_values(
            self,
            message: str,
            delay: int | float | None = None
    ) -> Sequence[int | float]:
        return self._resource.query_binary_values(message, delay)

