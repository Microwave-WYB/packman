import struct

from packman import nbytes, u8

# Using struct
data = b"\x01\x02"
a, b = struct.unpack("BB", data)
print(a, b)  # 1 2

# Using PackMan
fmt = u8 + u8
a, b, _ = fmt.unpack(data).flatten()
print(a, b)  # 1 2

# Complex example
fmt = u8 | (lambda length: u8 + nbytes(length - 1))
data = b"\x03\x01\x02\x03" + b"\x05\xff\x01\x02\x03\x04"
length, dtype, payload, _ = fmt.unpack(data).flatten()
print(length, dtype, payload)  # 3 1 b'\x02\x03'
