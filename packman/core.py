import struct
from copy import copy
from dataclasses import dataclass
from enum import StrEnum
from functools import cached_property
from typing import Callable, Literal, cast


class ByteOrder(StrEnum):
    # TODO: Support other byteorders, size, alignment formats
    NATIVE = "@"
    LITTLE = "<"
    BIG = ">"


@dataclass
class UnpackResult[*T]:
    values: tuple[*T]
    rest: bytes

    def unwrap(self) -> tuple[*T, bytes]:
        return *self.values, self.rest


class PackFormat[*T]:
    fmt: str
    byteorder: ByteOrder = ByteOrder.NATIVE

    def __init__(
        self, byteorder: ByteOrder | Literal["little", "big", "native"] = "native"
    ) -> None:
        if isinstance(byteorder, ByteOrder):
            self.byteorder = byteorder
        else:
            self.byteorder = {
                "little": ByteOrder.LITTLE,
                "big": ByteOrder.BIG,
                "native": ByteOrder.NATIVE,
            }[byteorder]

    @cached_property
    def size(self) -> int:
        return struct.calcsize(self.fmt)

    def unpack(self, data: bytes) -> UnpackResult[*T]:
        fmt = f"{self.byteorder}{self.fmt}"
        values = struct.unpack(fmt, data[: self.size])
        rest = data[self.size :]
        return UnpackResult(values, rest)

    def pack(self, *values: *T) -> bytes:
        return struct.pack(self.fmt, *values)

    def __add__[*U](self, other: "PackFormat[*U]") -> "PackFormat[(*T, *U)]":
        new_format = copy(self)
        new_format.fmt = (
            f"{self.fmt}{other.byteorder if self.byteorder != other.byteorder else ''}{other.fmt}"
        )
        return cast("PackFormat[(*T, *U)]", new_format)

    def then[*U](self, mapper: Callable[[*T], "PackFormat[*U]"]) -> "PackFormat[(*T, *U)]":
        class Chainedformat(PackFormat):
            def __init__(self, first: PackFormat, mapper: Callable):
                super().__init__()
                self.first = first
                self.mapper = mapper

            def unpack(self, data: bytes) -> UnpackResult[(*T, *U)]:
                first_result = self.first.unpack(data)
                second_format = self.mapper(*first_result.values)
                second_result = second_format.unpack(first_result.rest)
                return UnpackResult(
                    (*first_result.values, *second_result.values), second_result.rest
                )

            def pack(self, *values) -> bytes:
                first_fmt = f"{self.first.byteorder}{self.first.fmt}"
                first_size = struct.calcsize(first_fmt)
                first_values = values[:first_size]
                remaining_values = values[first_size:]

                first_packed = self.first.pack(*first_values)
                second_format = self.mapper(*first_values)
                second_packed = second_format.pack(*remaining_values)

                return first_packed + second_packed

        return Chainedformat(self, mapper)

    def __or__[*U](self, mapper: Callable[[*T], "PackFormat[*U]"]) -> "PackFormat[(*T, *U)]":
        return self.then(mapper)
