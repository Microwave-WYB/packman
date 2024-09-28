from packman.core import ByteOrder, ByteOrderName, ByteOrderSymbol, PackFormat
from packman.result import UnpackResult


class U8(PackFormat[int]):
    fmt = "B"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class U16(PackFormat[int]):
    fmt = "H"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class U32(PackFormat[int]):
    fmt = "I"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class U64(PackFormat[int]):
    fmt = "Q"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class I8(PackFormat[int]):
    fmt = "b"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class I16(PackFormat[int]):
    fmt = "h"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class I32(PackFormat[int]):
    fmt = "i"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class I64(PackFormat[int]):
    fmt = "q"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class Usize(PackFormat[int]):
    fmt = "N"

    def __init__(self) -> None:
        super().__init__(self.fmt)

    def unpack(
        self,
        data: bytes,
        byteorder: ByteOrder | ByteOrderName | ByteOrderSymbol = ByteOrder.NATIVE_ALIGNED,
    ) -> UnpackResult[int]:
        byteorder = byteorder if isinstance(byteorder, ByteOrder) else ByteOrder.from_str(byteorder)
        if byteorder != ByteOrder.NATIVE_ALIGNED:
            raise ValueError(
                f"Unsupported byteorder {byteorder} for Usize. Only {ByteOrder.NATIVE_ALIGNED} is supported."
            )
        return super().unpack(data, byteorder)


class Isize(PackFormat[int]):
    fmt = "n"

    def __init__(self) -> None:
        super().__init__(self.fmt)

    def unpack(
        self,
        data: bytes,
        byteorder: ByteOrder | ByteOrderName | ByteOrderSymbol = ByteOrder.NATIVE_ALIGNED,
    ) -> UnpackResult[int]:
        byteorder = byteorder if isinstance(byteorder, ByteOrder) else ByteOrder.from_str(byteorder)
        if byteorder != ByteOrder.NATIVE_ALIGNED:
            raise ValueError(
                f"Unsupported byteorder {byteorder} for Usize. Only {ByteOrder.NATIVE_ALIGNED} is supported."
            )
        return super().unpack(data, byteorder)


class F16(PackFormat[float]):
    fmt = "e"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class F32(PackFormat[float]):
    fmt = "f"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class F64(PackFormat[float]):
    fmt = "d"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class Char(PackFormat[bytes]):
    fmt = "c"

    def __init__(self) -> None:
        super().__init__(self.fmt)


class Bytes(PackFormat[bytes]):
    def __init__(self, length: int = 1) -> None:
        self._length = length
        self.fmt = f"{length}s" if length > 1 else "s"
        super().__init__(self.fmt)
