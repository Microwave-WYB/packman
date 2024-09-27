import struct


class UnpackError(Exception):
    """Raised when there is an error unpacking data."""

    def __init__(self, data: bytes, fmt: str, msg: str | None = None) -> None:
        self.data = data
        self.fmt = fmt
        self.msg = (
            f"{msg}\n"
            f"    Data   ({len(data)} bytes): {list(data)}\n"
            f"    Format ({struct.calcsize(fmt)} bytes): {fmt}"
        )
        super().__init__(self.msg)
