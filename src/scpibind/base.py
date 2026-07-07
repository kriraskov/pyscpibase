from enum import Enum
from pyvisa import ResourceManager
from typing import Any, Self, TypeVar, Generic


T = TypeVar("T")


class ResourceBase:
    def __init__(self, resource_name: str, rm: ResourceManager | None = None,
                 **resource_kwargs) -> None:
        self.resource_name = resource_name
        self.rm = rm or ResourceManager()
        self.resource_kwargs = resource_kwargs
        self._resource = None

    def __getattr__(self, name: str) -> Any:
        if self._resource is None:
            raise RuntimeError("Resource is not open.")
        return getattr(self._resource, name)

    def __enter__(self) -> Self:
        return self.open()

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: object | None) -> None:
        self.close()

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

    def setup(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"{key} is not a valid attribute.")


class SCPIProperty(Generic[T]):
    def __init__(self, get_cmd: str, set_cmd: str | None = None,
                 type_: type[T] = str) -> None:
        self.get_cmd = get_cmd
        self.set_cmd = set_cmd or get_cmd.removesuffix("?")
        self.type_ = type_  # str, float, int, Enum

    def __get__(self, resource: ResourceBase | None, owner: type) -> T | Self:
        if resource is None:
            return self
        message = resource.query(self.get_cmd).strip()
        return self.type_(message)

    def __set__(self, resource: ResourceBase, value: T) -> None:
        if isinstance(value, Enum):
            value = value.value
        resource.write(f"{self.set_cmd} {value}")


class Instrument(ResourceBase):
    identity = SCPIProperty("*IDN?")
    complete = SCPIProperty("*OPC?", type_=int)

    def reset(self):
        self.write("*RST")

    def clear(self):
        self.write("*CLS")

    def wait(self):
        self.write("*WAI")
