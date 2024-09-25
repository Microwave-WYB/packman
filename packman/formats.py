from packman.core import PackFormat


class U8(PackFormat[int]):
    fmt = "B"


class U16(PackFormat[int]):
    fmt = "H"


class U32(PackFormat[int]):
    fmt = "I"


class U64(PackFormat[int]):
    fmt = "Q"


class I8(PackFormat[int]):
    fmt = "b"


class I16(PackFormat[int]):
    fmt = "h"


class I32(PackFormat[int]):
    fmt = "i"


class I64(PackFormat[int]):
    fmt = "q"


class F32(PackFormat[float]):
    fmt = "f"


class F64(PackFormat[float]):
    fmt = "d"


class Char(PackFormat[bytes]):
    fmt = "c"


class Bytes(PackFormat[bytes]):
    def __init__(self, length: int = 1) -> None:
        super().__init__()
        self._length = length
        self.fmt = f"{length}s" if length > 1 else "s"
