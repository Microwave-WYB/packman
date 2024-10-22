import struct
from copy import copy
from dataclasses import dataclass
from enum import StrEnum
from typing import Callable, Literal, cast

from packman.error import UnpackError
from packman.result import UnpackResult

type ByteOrderName = Literal["native", "native_aligned", "little", "big", "network"]
type ByteOrderSymbol = Literal["=", "@", "<", ">", "!"]


class ByteOrder(StrEnum):
    NATIVE = "="
    NATIVE_ALIGNED = "@"
    LITTLE = "<"
    BIG = ">"
    NETWORK = "!"

    @classmethod
    def from_str(
        cls: type["ByteOrder"],
        value: ByteOrderName | ByteOrderSymbol,
    ) -> "ByteOrder":
        if value in cls:
            return ByteOrder(value)
        return {
            "native": cls.NATIVE,
            "native_aligned": cls.NATIVE_ALIGNED,
            "little": cls.LITTLE,
            "big": cls.BIG,
            "network": cls.NETWORK,
        }[value]


@dataclass
class PackFormat[*T]:
    """
    Basic binary packing format.

    With byteorder set to ByteOrder.NONE, the format will inherit previously defined byteorder, if any.
    If not, it will default to ByteOrder.NATIVE_ALIGNED, which is the same as the struct module.
    """

    fmt: str

    def unpack(
        self,
        data: bytes,
        byteorder: ByteOrder | ByteOrderName | ByteOrderSymbol = ByteOrder.NATIVE_ALIGNED,
    ) -> UnpackResult[*T]:
        """
        Unpacks data into an UnpackResult object.
        >>> from packman import U8
        >>> U8().unpack(b"\x01").expand()
        (1, b'')
        """
        byteorder = byteorder if isinstance(byteorder, ByteOrder) else ByteOrder.from_str(byteorder)
        fmt = f"{byteorder}{self.fmt}"
        size = struct.calcsize(fmt)
        try:
            values = struct.unpack(fmt, data[:size])
            rest = data[size:]
            return UnpackResult(values, rest)
        except struct.error as e:
            raise UnpackError(data, fmt, str(e)) from e

    def pack(
        self,
        *values: *T,
        byteorder: ByteOrder | ByteOrderName | ByteOrderSymbol = ByteOrder.NATIVE_ALIGNED,
    ) -> bytes:
        """
        Packs values into bytes.
        >>> from packman import U8
        >>> U8().pack(1).hex()
        '01'
        """
        fmt = f"{byteorder}{self.fmt}"
        return struct.pack(fmt, *values)

    def __add__[*U](self, other: "PackFormat[*U]") -> "PackFormat[(*T, *U)]":
        """
        Describes the concatenation of two formats.
        >>> from packman import U8
        >>> (U8() + U8()).fmt
        'BB'
        >>> (U8() + U8()).unpack(b"\x01\x02").expand()
        (1, 2, b'')
        """
        return PackFormat[(*T, *U)](f"{self.fmt}{other.fmt}")

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
            try:
                second_result = second_format.unpack(first_result.rest)
                return UnpackResult(
                    (*first_result.values, *second_result.values), second_result.rest
                )
            except struct.error as e:
                raise UnpackError(data, self.first.fmt + second_format.fmt, str(e)) from e

        def new_pack(self, *values) -> bytes:
            first_size = struct.calcsize(self.first.fmt)
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
