from typing import Any, Dict, Optional

from umsgpack import Ext, dumps, loads

from ._resolver import Resolver

__all__ = ("Packer",)


class Packer:
    """
    Handles the packing and unpacking of objects into and from byte representations.

    This class utilizes a `Resolver` to handle the conversion of objects into
    serializable formats, and vice versa, using message pack.
    """

    def __init__(self, resolver: Resolver) -> None:
        """
        Initialize the `Packer` with the given resolver.

        :param resolver: The resolver used to register and look up classes for packing
                         and unpacking.
        """
        self._resolver = resolver

    def _pack(self, packable: Any) -> Ext:
        """
        Pack an object into an `Ext` type with a class name and packed data.

        :param packable: The object to be packed.
        :return: A message pack `Ext` object representing the packed data.
        """
        cls_name = self._resolver.resolve_name(type(packable))
        return Ext(0x42, self.pack([cls_name, packable.__packed__()]))

    def pack(self, packable: Any) -> bytes:
        """
        Serialize the given object into a bytes representation.

        :param packable: The object to be packed.
        :return: A bytes object representing the packed data.
        """
        return dumps(packable, ext_handlers={object: self._pack})  # type: ignore

    def _unpack(self, packed: bytes, ext_resolvers: Dict[Any, Any]) -> Any:
        """
        Unpack a custom `Ext` object into its original form.

        :param packed: The packed bytes to be unpacked.
        :param ext_resolvers: A dictionary of external resolvers for specific types.
        :return: The unpacked object.
        """
        cls_name, kwargs = self.unpack(packed, ext_resolvers)
        resolved = self._resolver.resolve_type(cls_name)

        for cls, resolver in ext_resolvers.items():
            if issubclass(resolved, cls):
                return resolver(resolved, **kwargs)

        if hasattr(resolved, "__unpacked__"):
            return resolved.__unpacked__(**kwargs)
        return resolved(**kwargs)

    def unpack(self, packed: bytes, ext_resolvers: Optional[Dict[Any, Any]] = None) -> Any:
        """
        Deserialize the given packed bytes into the original object.

        :param packed: The bytes to be unpacked.
        :param ext_resolvers: A dictionary of external resolvers for specific types (optional).
        :return: The unpacked object.
        """
        return loads(packed, ext_handlers={
            0x42: lambda x: self._unpack(x.data, ext_resolvers or {}),
        })
