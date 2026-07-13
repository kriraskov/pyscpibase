from typing import Self, Generic, TypeVar, Callable
from enum import Enum
from src.scpibind.base import CommonBase


T = TypeVar("T")


class ReadOnly(Generic[T]):
    def __init__(self, get_cmd: str, type_: type[T] = str) -> None:
        self.get_cmd = get_cmd
        self.type_ = type_  # str, float, int, Enum

    def __get__(self, instance: CommonBase | None, owner: type) -> T | Self:
        if instance is None:
            return self
        message = instance.query(f"{instance.cmd_root}:{self.get_cmd}").strip()
        return self.type_(message)


class ReadWrite(ReadOnly[T]):
    def __init__(
            self,
            get_cmd: str,
            set_cmd: str | None = None,
            type_: type[T] = str
    ) -> None:
        super().__init__(get_cmd, type_)
        self.set_cmd = set_cmd or get_cmd.removesuffix("?")

    def __set__(self, instance: CommonBase, value: T) -> None:
        if isinstance(value, Enum):
            value = value.value
        instance.write(f"{instance.cmd_root}:{self.set_cmd} {value}")


class WriteOnly:
    def __init__(self, set_cmd: str) -> None:
        self.set_cmd = set_cmd

    def __get__(
            self,
            instance: CommonBase | None,
            owner: type
    ) -> Callable | Self:
        if instance is None:
            return self
        def bound(*args):
            if args:
                payload = ','.join(map(str, args))
                instance.write(f"{instance.cmd_root}:{self.set_cmd} {payload}")
            else:
                instance.write(f"{instance.cmd_root}:{self.set_cmd}")
        return bound
