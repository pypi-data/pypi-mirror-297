from typing import Any, Dict, Optional

from ._packable import Packable
from ._packer import Packer
from ._resolver import Resolver
from ._version import version

__version__ = version
__all__ = ("pack", "unpack", "packable",)


_resolver = Resolver()
_packer = Packer(_resolver)
packable = Packable(_resolver)


def pack(packable: Any) -> bytes:
    """
    Pack the given object into a byte representation.

    This function serializes a given `packable` object using the `Packer`
    and returns a bytes representation.

    :param packable: The object to be packed.
    :return: A bytes object representing the packed data.
    """
    return _packer.pack(packable)


def unpack(packed: bytes, ext_resolvers: Optional[Dict[Any, Any]] = None) -> Any:
    """
    Unpack the given byte data back into an object.

    This function deserializes the `packed` bytes into the original object.
    Optionally, external resolvers can be provided to handle specific types.

    :param packed: The byte data to be unpacked.
    :param ext_resolvers: A dictionary of external resolvers for specific types (optional).
    :return: The unpacked object.
    """
    return _packer.unpack(packed, ext_resolvers)
