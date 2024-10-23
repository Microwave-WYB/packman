from typing import Final

from packman.core import PackFormat

u8: Final[PackFormat[int]] = PackFormat[int]("B")
u16: Final[PackFormat[int]] = PackFormat[int]("H")
u32: Final[PackFormat[int]] = PackFormat[int]("I")
u64: Final[PackFormat[int]] = PackFormat[int]("Q")
i8: Final[PackFormat[int]] = PackFormat[int]("b")
i16: Final[PackFormat[int]] = PackFormat[int]("h")
i32: Final[PackFormat[int]] = PackFormat[int]("i")
i64: Final[PackFormat[int]] = PackFormat[int]("q")
usize: Final[PackFormat[int]] = PackFormat[int]("N")
isize: Final[PackFormat[int]] = PackFormat[int]("n")
f16: Final[PackFormat[float]] = PackFormat[float]("e")
f32: Final[PackFormat[float]] = PackFormat[float]("f")
f64: Final[PackFormat[float]] = PackFormat[float]("d")
char: Final[PackFormat[bytes]] = PackFormat[bytes]("c")


def nbytes(length: int) -> PackFormat[bytes]:
    return PackFormat[bytes](f"{length}s")
