from dataclasses import dataclass


@dataclass
class UnpackResult[*T]:
    values: tuple[*T]
    rest: bytes

    def expand(self) -> tuple[*T, bytes]:
        return *self.values, self.rest

    def unwrap(self) -> tuple[tuple[*T], bytes]:
        return self.values, self.rest
