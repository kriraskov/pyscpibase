from adapters.visa_adapter import VISAAdapter
from src.scpibind.adapters.adapter import Adapter
from typing import Any


class CommonBase:
    def __init__(self, adapter: Adapter):
        self.adapter = adapter

    def __getattr__(self, name: str) -> Any:
        return getattr(self.adapter, name)


class Instrument(CommonBase):
    def __enter__(self) -> Adapter:
        return self.open()

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: object | None) -> None:
        self.close()

    @classmethod
    def from_resource(cls, resource_name: str) -> "Instrument":
        adapter = VISAAdapter(resource_name)
        return cls(adapter)

    def setup(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(
                    f"'{self.__class__.__name__}' has no attribute '{key}'."
                )
