from pyvisa import ResourceManager, log_to_screen
from typing import Any, Self, Protocol


class VISAInterface(Protocol):
    """Protocol for VISA interfaces."""
    def write(self, message: str) -> None:
        """Write a message to the resource.
        
        Args:
            message (str): Message to write to the resource.
        """
        ...

    def query(self, message: str) -> str:
        """Write a message to the resource and query the response.
        
        Args:
            message (str): Message to write to the resource.
        
        Returns:
            str: Response from the resource.
        """
        ...


class SCPIProperty:
    def __init__(self, get_cmd: str, set_cmd: str | None = None,
                 typecast: type = str):
        self.get_cmd = get_cmd
        self.set_cmd = set_cmd or get_cmd.replace("?", "")
        self.typecast = typecast

    def __get__(self, instance: VISAInterface, owner: type):
        if instance is None:
            return self

        get_cmd = self.get_cmd.format(**vars(instance))

        return self.typecast(instance.query(get_cmd))
    
    def __set__(self, instance: VISAInterface, value: Any) -> None:
        set_cmd = self.set_cmd.format(**vars(instance))
        instance.write(f"{set_cmd} {value}")


class ResourceBase:
    def __init__(self, resource_name: str, rm: ResourceManager | None = None,
                 log_to_screen: bool = False, **kwargs) -> None:
        self.resource_name = resource_name
        self._rm = rm or ResourceManager()
        self._resource = None
        self._log_to_screen = log_to_screen
        self._kwargs = kwargs

    def __getattr__(self, name: str) -> Any:
        getattr(self.resource, name)

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
                self._kwargs
            )
        if self._log_to_screen:
            log_to_screen()
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


class Instrument(ResourceBase):
    identity = SCPIProperty("*IDN?")
    complete = SCPIProperty("*OPC?")

    def reset(self):
        self.write("*RST")

    def clear(self):
        self.write("*CLS")

    def wait(self):
        self.write("*WAI")


class SubSystem:
    """Represents an SCPI subsystem for an instrument.

    Attributes:
        instrument (Instrument): The instrument instance to which the
            subsystem belongs.
        suffix (int): Subsystem suffix.
    """
    def __init__(self, instrument: Instrument, suffix: int) -> None:
        """Initialize the channel.
        
        Args:
            instrument (Instrument): The instrument instance to which
                the subsystem belongs.
            suffix (int): Subsystem suffix.
        """
        self.instrument = instrument
        self.suffix = suffix

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the instrument instance.
        
        Args:
            name (str): Name of the attribute to access.
        
        Returns:
            Any: The attribute value from the instrument instance.
        """
        return getattr(self.instrument, name)

    def setup(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(
                    f"{key} is not a valid attribute of "
                    f"{self.__class__.__name__}"
                )
