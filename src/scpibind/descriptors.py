from typing import Self, Generic, TypeVar, Callable
from enum import Enum
from base import CommonBase


T = TypeVar("T")


class ReadOnly(Generic[T]):
    def __init__(self, get_cmd: str, type_: type[T] = str, **kwargs) -> None:
        self.get_cmd = get_cmd
        self.type_ = type_  # str, float, int, Enum
        self.kwargs  = kwargs

    def __get__(self, instance: CommonBase | None, owner: type) -> T | Self:
        if instance is None:
            return self
        message = instance.query(
            f"{instance.cmd_root}{self.get_cmd}",
            **self.kwargs
        )
        return self.type_(message.strip())


class ReadWrite(ReadOnly[T]):
    def __init__(
            self,
            get_cmd: str,
            set_cmd: str | None = None,
            type_: type[T] = str,
            **kwargs
    ) -> None:
        super().__init__(get_cmd, type_)
        self.set_cmd = set_cmd or get_cmd.removesuffix("?")

    def __set__(self, instance: CommonBase, value: T) -> None:
        if isinstance(value, Enum):
            value = value.value
        instance.write(
            f"{instance.cmd_root}{self.set_cmd} {value}",
            **self.kwargs
        )


class ReadBinary:
    def __init__(self, get_cmd: str, **kwargs) -> None:
        self.get_cmd = get_cmd
        self.kwargs = kwargs

    def __get__(
            self,
            instance: CommonBase | None,
            owner: type
    ) -> Callable | Self:
        if instance is None:
            return self
        def bound():
            instance.query_binary_value(
                f"{instance.cmd_root}{self.get_cmd}",
                **self.kwargs
            )
        return bound


class WriteOnly:
    def __init__(self, set_cmd: str, **kwargs) -> None:
        self.set_cmd = set_cmd
        self.kwargs = kwargs

    def __get__(
            self,
            instance: CommonBase | None,
            owner: type
    ) -> Callable | Self:
        if instance is None:
            return self
        def bound():
            instance.write(
                f"{instance.cmd_root}{self.set_cmd}",
                **self.kwargs
            )
        return bound


class ParameterizedWriteOnly:
    def __init__(self, set_cmd: str, **kwargs) -> None:
        self.set_cmd = set_cmd
        self.kwargs = kwargs

    def __get__(
            self,
            instance: CommonBase | None,
            owner: type
    ) -> Callable | Self:
        if instance is None:
            return self
        def bound(*args):
            payload = ','.join(map(str, args))
            instance.write(
                f"{instance.cmd_root}{self.set_cmd} {payload}",
                **self.kwargs
            )
        return bound
