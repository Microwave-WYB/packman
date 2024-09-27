# Packman: Pythonic Binary Packing/Unpacking Like a Super Hero

![intro](/images/intro.png)

> [!WARNING]
>
> This tool is under heavy developments and should not be used in production code.

PackMan is a flexible and intuitive library for packing and unpacking binary data in Python. It provides a more Pythonic and type-safe alternative to the built-in `struct` module, with additional features for chaining and dynamic format creation.

## Installation

Minimum Python version: `3.12`

This libarry uses the [PEP695](https://peps.python.org/pep-0695) type parameter syntax introduce in Python `3.12`.

```sh
# pip install packman  # TODO: publish to PyPI
pip install git+https://github.com/Microwave-WYB/packman.git
```

## Basic Usage

### Simple Unpacking

Let's start with a basic example comparing PackMan to the built-in `struct` module:

```python
import struct
from packman import U8

# Using struct
data = b'\x01\x02'
a, b = struct.unpack('BB', data)
print(a, b)  # 1 2

# Using PackMan
fmt = U8() + U8()
a, b, _ = fmt.unpack(data).expand()
print(a, b)  # 1 2
```

PackMan offers improved type safety: returned value from struct.unpack has type `tuple[Any, ...]`, while PackMan's return value has the more specific type `tuple[int, int, bytes]`, providing better type information and reducing the risk of type-related errors.

![type_demo](/images/type_demo.png)

### Working with `UnpackResult`

`unpack` will return an `UnpackResult` object. There are several ways to get the data:

```python
data = b'\x01\x02\x03'
fmt = U8() + U8()

# result only:
a, b = fmt.unpack(data).values
print(a, b)  # 1 2

# remaining data only:
rest = fmt.unpack(data).rest
print(rest)  # b'\x03'

# result and remaining data (rest):
result, rest = fmt.unpack(data).unwrap()
print(result, rest)  # (1, 2) b'\x03'

(a, b), rest = fmt.unpack(data).unwrap()
print(a, b, rest)  # 1 2 b'\x03'

# expanded result and remaining data:
a, b, rest = fmt.unpack(data).expand()
print(a, b, rest)  # 1 2 b'\x03'
```

You will find `.expand()` very useful in simplifying the syntax if you need to unpack individual results and keep working on the remaining data.

### Packing and Unpacking

PackMan allows you to easily define formats and use them for both packing and unpacking:

```python
from packman import U8, Bytes

fmt = U8() + U8() + Bytes(1)

# Packing
packed = fmt.pack(1, 2, b"a")
print(packed)  # b'\x01\x02a'

# Unpacking
unpacked = fmt.unpack(packed).expand()
print(unpacked)  # (1, 2, b'a', b'')
```

## Advanced Usage

### Dynamic Formats

PackMan supports dynamic format creation based on previous values:

```python
from packman import U8, Bytes

fmt = U8() | (lambda length: U8() + Bytes(length - 1))

# Packing
packed = fmt.pack(3, 1, b"\x02\x03")
print(packed)  # b'\x03\x01\x02\x03'

# Unpacking
unpacked = fmt.unpack(packed).expand()
print(unpacked)  # (3, 1, b'\x02\x03', b'')
```

### Parsing Iterators

PackMan can be used to create efficient parsers for complex data structures:

```python
from packman import U8, Bytes
from collections.abc import Iterator

# Regular unpacking:
def parse_ble_advertisement(data: bytes) -> Iterator[tuple[int, int, bytes]]:
    while data:
        length, data = U8().unpack(data).expand()
        dtype, payload, data = (U8() + Bytes(length - 1)).unpack(data).expand()
        yield length, dtype, payload

# Dynamic format unpacking:
def parse_ble_advertisement(data: bytes) -> Iterator[tuple[int, int, bytes]]:
    fmt = U8() | (lambda length: U8() + Bytes(length - 1))
    while data:
        length, dtype, payload, data = fmt.unpack(data).expand()
        yield length, dtype, payload

# Usage
example_ble_ad = b"\x03\x01\x02\x03" + b"\x05\xff\x01\x02\x03\x04"
for length, dtype, payload in parse_ble_advertisement(example_ble_ad):
    print(f"Length: {length}, Type: {dtype}, Payload: {payload.hex()}")
```

## Features

-   Pythonic API for binary packing and unpacking
-   Type-safe operations with Python's type hints
-   Support for dynamic format creation
-   Chaining of formats for complex data structures
-   Efficient parsing of iterative data structures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
