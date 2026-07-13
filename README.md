# scpi-bind

SCPI instrument abstraction with property binding built around PyVISA.

## Features
 - Object-oriented SCPI instrument interfaces
 - Property binding for SCPI commands
 - Sub-system interfaces

## Installation

```bash
pip install scpi-bind
```

## Example

```python
from src.scpibind.base import Instrument, SubSystem
from src.scpibind.descriptors import ReadWrite
from enum import Enum


class State(Enum):
    ON = "ON"
    OFF = "OFF"


class Channel(SubSystem):
    cmd_root = "SOUR:CHAN"
    
    # Add a property with query and write commands
    voltage = ReadWrite(get_cmd="VOLT?", set_cmd="VOLT", type_=float)
    
    # Automatically remove '?' if no 'set_cmd' is given
    current = ReadWrite("CURR?", type_=float)


class PowerSupply(Instrument):
    beep = ReadWrite("SYST:BEEP", type_=State)
    
    def __init__(self, adapter):
        super().__init__(adapter)
        self.channel = SubSystem(adapter)
        
        
with PowerSupply.from_resource("TCPIP0::192.168.0.10::INSTR") as psu:
    print(psu.identity)

    # Modify a property
    psu.beep = State.ON
    
    # Set up multiple properties at the same time
    psu.channel[1].setup(voltage=5, current=0.1)
```

## License

MIT