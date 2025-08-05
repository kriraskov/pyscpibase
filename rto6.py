from .instrument import Instrument, SubSystem


class RTO6(Instrument):
    def __init__(
        self,
        resource_name: str,
        name: str = "RTO6",
        **kwargs
    ) -> None:
        super().__init__(resource_name, name, **kwargs)
        self.channel = [Channel(self, i + 1) for i in range(4)]
        self.math = [Math(self, i + 1) for i in range(8)]


class Channel(SubSystem):
    ...


class Math(SubSystem):
    ...
