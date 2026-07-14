from adapters.adapter import Adapter
from pyvisa import ResourceManager
from typing import Self, Sequence


class VISAAdapter(Adapter):
    def __init__(
            self,
            resource_name: str,
            rm: ResourceManager | None = None,
            **kwargs
    ) -> None:
        self.resource_name = resource_name
        self.rm = rm or ResourceManager()
        self.kwargs = kwargs
        self._resource = None

    def open(self) -> Self:
        if self._resource is None:
            self._resource = self.rm.open_resource(
                self.resource_name,
                **self.kwargs
            )
        return self

    def close(self):
        if self._resource is not None:
            self._resource.close()
            self._resource = None

    def read(self, **kwargs) -> str:
        return self._resource.read(**kwargs)

    def read_binary_values(self, **kwargs) -> Sequence[int | float]:
        return self._resource.read_binary_values(**kwargs)

    def write(self, message: str, **kwargs) -> None:
        self._resource.write(message, **kwargs)

    def write_binary_values(
            self,
            message: str,
            values: Sequence[int | float],
            **kwargs
    ) -> None:
        self._resource.write_binary_values(message, values, **kwargs)

    def query(self, message: str, delay: int | float | None = None) -> None:
        return self._resource.query(message, delay)

    def query_binary_values(
            self,
            message: str,
            delay: int | float | None = None,
            **kwargs
    ) -> Sequence[int | float]:
        return self._resource.query_binary_values(message, delay, **kwargs)

