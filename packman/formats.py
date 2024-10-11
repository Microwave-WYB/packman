from packman.core import PackFormat

u8 = PackFormat[int]("B")
u16 = PackFormat[int]("H")
u32 = PackFormat[int]("I")
u64 = PackFormat[int]("Q")
i8 = PackFormat[int]("b")
i16 = PackFormat[int]("h")
i32 = PackFormat[int]("i")
i64 = PackFormat[int]("q")
usize = PackFormat[int]("N")
isize = PackFormat[int]("n")
f16 = PackFormat[float]("e")
f32 = PackFormat[float]("f")
f64 = PackFormat[float]("d")
char = PackFormat[bytes]("c")


def nbytes(length: int) -> PackFormat[bytes]:
    return PackFormat[bytes](f"{length}c")
