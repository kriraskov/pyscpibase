from adapters.visa_adapter import VISAAdapter
from src.scpibind.adapters.adapter import Adapter
from src.scpibind.descriptors import ReadWrite
from typing import Any, Self


class CommonBase:
    cmd_root: str = ""

    def __init__(self, adapter: Adapter, cmd_root: str | None = None) -> None:
        self.adapter = adapter
        if cmd_root is not None:
            self.cmd_root = cmd_root

    def __getattr__(self, name: str) -> Any:
        return getattr(self.adapter, name)

    def setup(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key in vars(self):
                setattr(self, key, value)
            else:
                raise AttributeError(
                    f"'{self.__class__.__name__}' has no attribute '{key}'."
                )


class Instrument(CommonBase):
    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: object | None
    ) -> None:
        self.close()

    @classmethod
    def from_resource(cls, resource_name: str) -> Self:
        adapter = VISAAdapter(resource_name)
        return cls(adapter)


class SubSystem(CommonBase):
    def __getitem__(self, item: int) -> Self:
        return self.__class__(self.adapter, cmd_root=f"{self.cmd_root}{item}")
