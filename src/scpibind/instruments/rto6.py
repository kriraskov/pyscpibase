from base import Instrument, SubSystem
from adapters.adapter import Adapter
from descriptors import ReadWrite, WriteOnly, ReadOnly, ReadBinary
from enum import Enum
import numpy as np


class State(Enum):
    ON = "ON"
    OFF = "OFF"


class Format(Enum):
    ASCII = "ASC"
    REAL32 = "REAL,32"
    REAL64 = "REAL,64"
    INT8 = "INT,8"
    INT16 = "INT,16"


class Coupling(Enum):
    DC50 = "DC"
    DC1M = "DCL"
    AC1M = "AC"


class FFTType(Enum):
    MAGNITUDE = "MAGN"
    PHASE = "PHAS"


class FFTScale(Enum):
    LINEAR = "LIN"
    LOGARITHMIC = "LOG"


class FFTWindow(Enum):
    RECTANGULAR = "RECT"
    HAMMING = "HAMM"
    HANN = "HANN"
    BLACKMANHARRIS = "BLACK"
    GAUSSIAN = "GAUS"
    FLATTOP = "FLAT"
    KAISER = "KAIS"


class RTO6(Instrument):
    format = ReadWrite("FORM?", type_=Format)
    update_display = ReadWrite("SYST:DISP:UPD?", type_=State)
    run_single = WriteOnly("RUNS")

    def __init__(self, adapter: Adapter):
        super().__init__(adapter)
        self.channel = Channel(adapter)
        self.math = Math(adapter)
        self.fft = FFT(adapter)


class Channel(SubSystem):
    cmd_root = "CHAN"

    status = ReadWrite("STAT?", type_=State)
    coupling = ReadWrite("COUP?", type_=Coupling)


class Math(SubSystem):
    cmd_root = "CALC:MATH"

    status = ReadWrite("STAT?", type_=State)
    expression = ReadWrite("EXPR?", type_=str)
    range = ReadWrite("VERT:RANG?", type_=float)
    header = ReadOnly("DATA:HEAD?", type_=str)

    get_data = ReadBinary(
        "DATA?",
        datatype="f",
        container=np.array
    )


class FFT(SubSystem):
    cmd_root = "CALC:MATH"

    type = ReadWrite("FFT:TYPE?", type_=FFTType)
    scale = ReadWrite("FFT:LOGS?", type_=FFTScale)
    window = ReadWrite("FFT:WIND:TYPE?", type_=FFTWindow)
    start = ReadWrite("FFT:START?", type_=float)
    stop = ReadWrite("FFT:STOP?", type_=float)
    bandwidth = ReadWrite("FFT:BAND?", type_=float)
    level = ReadWrite("FFT:MAGN:LEV?", type_=float)
    count = ReadWrite("FFT:FRAM:MAXC?", type_=int)
    overlap = ReadWrite("FFT:FRAM:OFAC?", type_=float)
