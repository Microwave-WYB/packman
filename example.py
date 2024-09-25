import struct

from packman import U8, Bytes

# Using struct
data = b"\x01\x02"
a, b = struct.unpack("BB", data)
print(a, b)  # 1 2

# Using PackMan
fmt = U8() + U8()
a, b, _ = fmt.unpack(data).expand()
print(a, b)  # 1 2

# Complex example
fmt = U8() | (lambda length: U8() + Bytes(length - 1))
data = b"\x03\x01\x02\x03" + b"\x05\xff\x01\x02\x03\x04"
length, dtype, payload, _ = fmt.unpack(data).expand()
print(length, dtype, payload)  # 3 1 b'\x02\x03'
