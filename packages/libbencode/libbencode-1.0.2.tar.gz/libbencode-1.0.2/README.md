# libbencode

A Python library for Bencode encoding and decoding.

# Installation

Installing through pip:
```bash
pip install libbencode
```

Installing through source:
```bash
git clone https://github.com/zrekryu/libbencode.git
cd libbencode
pip install .
```

# Usage

## Decoding
```py
import libbencode

data: bytes = b'i42e'  # bencode integer.
decoded_data: int = libbencode.decode(data)
print(decoded_data)  # 42
```
## Encoding
```py
import libbencode

data: int = 42  # python integer.
encoded_data: bytes = libbencode.encode(data)
print(encoded_data)  # b'i42e'
```

## Version Information

To print the version of the `libbencode` library:
```py
import libbencode

print(libbencode.__version__)
```

# Bencode API

## Decoding API

All `decode_*` methods return a tuple of the decoded data and the position of the end byte in the data.

### Decoding an Integer

Decodes an integer from bencode format:
```py
from libbencode import Decoder

data: bytes = b"i42e"
decoded_data: tuple[int, int] = Decoder.decode_int(data)
print(decoded_data)  # (42, 3)
```

### Decoding a String

Decodes a string from bencode format:
```py
from libbencode import Decoder

data: bytes = b"4:spam"
decoded_data: tuple[bytes, int] = Decoder.decode_str(data)
print(decoded_data)  # (b'spam', 5)
```

Decoding with a specific encoding:
```py
decoded_data: tuple[str, int] = Decoder.decode_str(data, encoding="utf-8")  # ('spam', 5)
```

### Decoding a List

Decodes a list from bencode format:
```py
from libbencode import Decoder

data: bytes = b"l4:spami42ee"
decoded_data: tuple[list[bytes | int], int] = Decoder.decode_list(data)
print(decoded_data)  # ([b'spam', 42], 11)
```

Decoding with a specific encoding:
```py
decoded_data: tuple[list[str | int], int] = Decoder.decode_list(data, encoding="utf-8")  # (['spam', 42], 21)
```

### Decoding a Dictionary

Decodes a dictionary from bencode format:
```py
from libbencode import Decoder

data: bytes = b"d3:bar4:spam3:fooi42ee"
decoded_data: tuple[dict[bytes, bytes | int]] = Decoder.decode_dict(data)
print(decoded_data)  # ({b'bar': b'spam', b'foo': 42}, 21)
```

Decoding with a specific encoding:
```py
decoded_data: tuple[dict[str, str | int], int] = Decoder.decode_dict(data, encoding="utf-8")  # {'bar': 'spam', 'foo': 42}
```

## Encoding API

### Encoding an Integer
```py
from libbencode import Encoder

data: int = 42
encoded_data: bytes = Encoder.encode_int(data)
print(encoded_data)  # b'i42e'
```

### Encoding Bytes

Encodes bytes into bencode format:
```py
from libbencode import Encoder

data: bytes = b"spam"
encoded_data: bytes = Encoder.encode_bytes(data)
print(encoded_data)  # b'4:spam'
```

### Encoding a String

Encodes a string into bencode format:
```py
from libbencode import Encoder

data: str = "spam"
encoded_data: bytes = Encoder.encode_str(data)
print(encoded_data)  # b'4:spam'
```

### Encoding a List

Encodes a list into bencode format:
```py
from libbencode import Encoder

data: list[str | int] = ["spam", 42]
encoded_data: bytes = Encoder.encode_list(data)
print(encoded_data)  # b'l4:spami42ee'
```

### Encoding a Dictionary

Encodes a dictionary into bencode format:
```py
from libbencode import Encoder

data: dict[str, str | int] = {"bar": "spam", "foo": 42}
encoded_data: bytes = Encoder.encode_dict(data)
print(encoded_data)  # b'd3:bar4:spam3:fooi42ee'
```

### Encoding a Boolean

The Bencode format does not natively support boolean values. Therefore, booleans are encoded as integers:

- True is encoded as `b'i1e'`
- False is encoded as `b'i0e'`

Encodes a boolean into bencode format:
```py
from libbencode import Encoder

data: bool = True
encoded_data: bytes = Encoder.encode_bool(data)
print(encoded_data)  # b'i1e'
```

# Tests

Tests are included in `tests` directory.

Run tests:
```bash
python -m unittest discover -s tests
```

# License

© 2024 Zrekryu. Licensed under MIT License. See the LICENSE file for details.