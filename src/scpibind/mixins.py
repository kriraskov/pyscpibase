from descriptors import ReadOnly, WriteOnly


class SCPIMixin:
    identity = ReadOnly("*IDN?")
    complete = ReadOnly("*OPC?", type_=int)

    reset = WriteOnly("*RST")
    clear = WriteOnly("*CLS")
    wait = WriteOnly("*WAI")
