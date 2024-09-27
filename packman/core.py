import struct
from copy import copy
from enum import StrEnum
from functools import cached_property
from typing import Callable, Literal, cast

from packman.result import UnpackResult

type ByteOrderName = Literal["none", "native", "native_aligned", "little", "big", "network"]


class ByteOrder(StrEnum):
    NONE = ""
    NATIVE = "="
    NATIVE_ALIGNED = "@"
    LITTLE = "<"
    BIG = ">"
    NETWORK = "!"

    @classmethod
    def from_name(
        cls: type["ByteOrder"],
        name: ByteOrderName,
    ) -> "ByteOrder":
        return {
            "none": cls.NONE,
            "native": cls.NATIVE,
            "native_aligned": cls.NATIVE_ALIGNED,
            "little": cls.LITTLE,
            "big": cls.BIG,
            "network": cls.NETWORK,
        }[name]


class PackFormat[*T]:
    """
    Basic binary packing format.

    With byteorder set to ByteOrder.NONE, the format will inherit previously defined byteorder, if any.
    If not, it will default to ByteOrder.NATIVE_ALIGNED, which is the same as the struct module.
    """

    fmt: str
    byteorder: ByteOrder = ByteOrder.NONE

    def __init__(
        self,
        byteorder: ByteOrder | ByteOrderName = ByteOrder.NONE,
    ) -> None:
        match byteorder:
            case ByteOrder(b):
                self.byteorder = b
            case _:
                self.byteorder = ByteOrder.from_name(byteorder)

    @cached_property
    def size(self) -> int:
        return struct.calcsize(
            f"{self.byteorder if self.byteorder != ByteOrder.NONE else ByteOrder.NATIVE_ALIGNED}{self.fmt}"
        )

    def unpack(self, data: bytes) -> UnpackResult[*T]:
        """
        Unpacks data into an UnpackResult object.
        >>> from packman import U8
        >>> U8().unpack(b"\x01").expand()
        (1, b'')
        """
        fmt = f"{self.byteorder if self.byteorder != ByteOrder.NONE else ByteOrder.NATIVE_ALIGNED}{self.fmt}"
        values = struct.unpack(fmt, data[: self.size])
        rest = data[self.size :]
        return UnpackResult(values, rest)

    def pack(self, *values: *T) -> bytes:
        """
        Packs values into bytes.
        >>> from packman import U8
        >>> U8().pack(1).hex()
        '01'
        """
        return struct.pack(self.fmt, *values)

    def __add__[*U](self, other: "PackFormat[*U]") -> "PackFormat[(*T, *U)]":
        """
        Describes the concatenation of two formats.
        >>> from packman import U8
        >>> (U8() + U8()).fmt
        'BB'
        >>> (U8() + U8()).unpack(b"\x01\x02").expand()
        (1, 2, b'')
        """
        new_format = copy(self)
        match new_format.byteorder, other.byteorder:
            case _, ByteOrder.NONE:
                new_format.fmt = f"{self.fmt}{other.fmt}"
            case byteorder, new_byteorder if byteorder != new_byteorder:
                new_format.fmt = f"{other.fmt}{new_byteorder}{self.fmt}"
            case _, _:
                new_format.fmt = f"{self.fmt}{other.fmt}"
        return cast("PackFormat[(*T, *U)]", new_format)

    def then[*U](self, mapper: Callable[[*T], "PackFormat[*U]"]) -> "PackFormat[(*T, *U)]":
        """
        Chains two formats, where the second format is dynamically derived from the result of the previous format.

        >>> from packman import U8, Bytes
        >>> U8().then(lambda length: Bytes(length)).unpack(b"\x01\x02").expand()
        (1, b'\\x02', b'')
        """
        new_format = copy(self)
        setattr(new_format, "first", self)
        setattr(new_format, "mapper", mapper)

        def new_unpack(self, data: bytes) -> UnpackResult[(*T, *U)]:
            first_result = self.first.unpack(data)
            second_format = self.mapper(*first_result.values)
            second_result = second_format.unpack(first_result.rest)
            return UnpackResult((*first_result.values, *second_result.values), second_result.rest)

        def new_pack(self, *values) -> bytes:
            first_fmt = f"{self.first.byteorder}{self.first.fmt}"
            first_size = struct.calcsize(first_fmt)
            first_values = values[:first_size]
            remaining_values = values[first_size:]

            first_packed = self.first.pack(*first_values)
            second_format = self.mapper(*first_values)
            second_packed = second_format.pack(*remaining_values)

            return first_packed + second_packed

        def new_add[*V](self, other: "PackFormat[*V]") -> "PackFormat[(*T, *V)]":
            """
            Chains this format with another format using a lambda function.
            The second format is applied regardless of the first format's values.

            >>> from packman import U8
            >>> (U8() + U8()).unpack(b"\x01\x02").expand()
            (1, 2, b'')
            """
            return self.then(lambda *_: other)

        new_format.unpack = new_unpack.__get__(new_format)
        new_format.pack = new_pack.__get__(new_format)
        new_format.__add__ = new_add.__get__(new_format)

        return cast("PackFormat[(*T, *U)]", new_format)

    def __or__[*U](self, mapper: Callable[[*T], "PackFormat[*U]"]) -> "PackFormat[(*T, *U)]":
        """Shorthand for `then`"""
        return self.then(mapper)
