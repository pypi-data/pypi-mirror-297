# packed

[![Codecov](https://img.shields.io/codecov/c/github/tsv1/packed/master.svg?style=flat-square)](https://codecov.io/gh/tsv1/packed)
[![PyPI](https://img.shields.io/pypi/v/packed.svg?style=flat-square)](https://pypi.python.org/pypi/packed/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/packed?style=flat-square)](https://pypi.python.org/pypi/packed/)
[![Python Version](https://img.shields.io/pypi/pyversions/packed.svg?style=flat-square)](https://pypi.python.org/pypi/packed/)

**packed** is a Python library that provides a simple way to serialize (pack) and deserialize (unpack) custom Python objects, leveraging the efficient [MessagePack](https://msgpack.org/) binary serialization format. It's designed to help you easily transmit objects over networks, save them to files, or perform any operation that requires converting objects to bytes and back.

## Features

- **Efficient Binary Serialization**: Uses [MessagePack](https://msgpack.org/), an efficient binary serialization format that's faster and smaller than JSON.
- **Simple Decorator-Based Registration**: Easily register your custom classes for packing and unpacking using the `@packable` decorator.
- **Customizable Serialization**: Define exactly what data gets serialized by implementing the `__packed__` method.
- **Supports Custom Unpacking Logic**: Use the `__unpacked__` class method to control how objects are reconstructed during unpacking.
- **Seamless Integration**: Works with standard Python types and custom objects, making it easy to integrate into existing projects.

## Installation

Install [packed](https://pypi.python.org/pypi/packed/) using `pip`:

```sh
pip3 install packed
```

## Quick Start

### Making a Class Packable

To make a custom class packable, decorate it with `@packable` and define a `__packed__` method that returns a dictionary of the attributes you want to serialize.

```python
from packed import packable

@packable  # Register the class for packing
class EqualMatcher:
    def __init__(self, expected):
        self._expected = expected

    def match(self, actual):
        return actual == self._expected

    def __packed__(self):  # Select the fields to pack
        return {"expected": self._expected}
```

### Packing Objects

Use the `pack` function to serialize an object into bytes.

**Client Side:**

```python
from packed import pack

matcher = EqualMatcher("banana")
packed_data = pack(matcher)
# You can now send 'packed_data' over a network or save it to a file
```

### Unpacking Objects

Use the `unpack` function to deserialize bytes back into an object.

**Server Side:**

```python
from packed import unpack

# Assume 'packed_data' is received from a network or read from a file
matcher = unpack(packed_data)
assert matcher.match("banana") is True
```

## Supported Data Types

**packed** supports serialization of the following standard Python data types:

- **Primitive Types**: `int`, `float`, `bool`, `None`, `str`, `bytes`
- **Collections**:
  - **Lists**: `[1, 2, 3]`
  - **Tuples**: `(1, 2, 3)`
  - **Dictionaries**: `{'key': 'value'}`
  - **Sets**: `{1, 2, 3}`
- **Nested Structures**: Collections containing other collections or primitive types.
- **Custom Objects**: Classes registered with the `@packable` decorator.

These types are serialized using MessagePack's built-in support for these data types, ensuring efficient and reliable serialization.

## How It Works

1. **Registration**: When you decorate a class with `@packable`, it gets registered with the internal resolver. This allows the `packed` library to keep track of which classes can be packed and unpacked.

2. **Packing**:
   - The `__packed__` method you define in your class specifies what data gets serialized.
   - The `pack` function uses this method to convert your object into a serializable form.
   - Metadata about the object's class is included to ensure it can be properly reconstructed.

3. **Unpacking**:
   - The `unpack` function reads the metadata and reconstructs the object.
   - If your class defines a `__unpacked__` class method, it will use that to create the object.
   - Otherwise, it will call the class constructor with the unpacked data.

## Advanced Usage

### Custom Unpacking Logic

If your class requires custom logic during unpacking, define a `__unpacked__` class method.

```python
@packable
class MyClass:
    def __init__(self, value):
        self.value = value

    def __packed__(self):
        return {'value': self.value}

    @classmethod
    def __unpacked__(cls, value):
        # Custom logic during unpacking
        instance = cls(value)
        instance.setup_additional_state()
        return instance

    def setup_additional_state(self):
        # Additional initialization
        pass
```

### Registering Classes with Custom Names

You can register a class with a custom name by passing the name to the decorator. This is useful if you need to avoid name collisions or want to use a different identifier.

```python
@packable("CustomName")
class MyClass:
    # Class definition
```

### Handling Subclasses

If you have a class hierarchy, register each subclass separately if you intend to pack and unpack them.

```python
@packable
class BaseClass:
    # Base class definition

@packable
class SubClass(BaseClass):
    # Subclass definition
```

## MessagePack

[MessagePack](https://msgpack.org/) is an efficient binary serialization format. It lets you exchange data among multiple languages like JSON but it's faster and smaller.

By using MessagePack under the hood, **packed** provides:

- **Efficiency**: Smaller message sizes and faster serialization/deserialization compared to text-based formats like JSON.
- **Interoperability**: Support for multiple languages, making it easier to integrate with systems written in different programming languages.
- **Simplicity**: A straightforward and easy-to-use API.

**packed** uses [umsgpack](https://github.com/vsergeev/u-msgpack-python), a pure Python implementation of MessagePack, for serialization and deserialization. This ensures that the library is lightweight and has minimal dependencies, making it easy to install and integrate.
