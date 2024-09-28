from packman.core import ByteOrder, ByteOrderName, PackFormat


class U8(PackFormat[int]):
    fmt = "B"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class U16(PackFormat[int]):
    fmt = "H"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class U32(PackFormat[int]):
    fmt = "I"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class U64(PackFormat[int]):
    fmt = "Q"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class I8(PackFormat[int]):
    fmt = "b"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class I16(PackFormat[int]):
    fmt = "h"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class I32(PackFormat[int]):
    fmt = "i"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class I64(PackFormat[int]):
    fmt = "q"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class F32(PackFormat[float]):
    fmt = "f"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class F64(PackFormat[float]):
    fmt = "d"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class Char(PackFormat[bytes]):
    fmt = "c"

    def __init__(self, byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE) -> None:
        super().__init__(self.fmt, byteorder)


class Bytes(PackFormat[bytes]):
    def __init__(self, length: int = 1) -> None:
        self._length = length
        self.fmt = f"{length}s" if length > 1 else "s"
        super().__init__(self.fmt)
