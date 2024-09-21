from collections import OrderedDict
from typing import Any, Dict, Optional, Type

__all__ = ("Resolver",)


AnyClass = Type[Any]


class Resolver:
    """
    Resolves classes by name and registers them for serialization.

    The `Resolver` class maintains a registry of class names and their
    corresponding class types, allowing the system to pack and unpack
    objects by resolving their types at runtime.
    """

    def __init__(self) -> None:
        """
        Initialize the `Resolver` with an empty registry.
        """
        self._registry: Dict[str, AnyClass] = OrderedDict()

    def register(self, cls: AnyClass, name: Optional[str] = None) -> None:
        """
        Register a class with the given name, or default to the class name.

        :param cls: The class to register.
        :param name: An optional name to register the class under (defaults to the class name).
        :raises KeyError: If the name is already registered.
        """
        if name is None:
            name = cls.__name__
        if name in self._registry:
            raise KeyError(name)
        self._registry[name] = cls

    def resolve_type(self, name: str) -> AnyClass:
        """
        Resolve the class type by its name.

        :param name: The name of the class to resolve.
        :return: The class type corresponding to the given name.
        :raises KeyError: If the name is not found in the registry.
        """
        if name not in self._registry:
            raise KeyError(name)
        return self._registry[name]

    def resolve_name(self, cls: AnyClass) -> str:
        """
        Resolve the class name by its type.

        :param cls: The class to resolve the name for.
        :return: The name corresponding to the class.
        :raises KeyError: If the class is not found in the registry.
        """
        for key, val in self._registry.items():
            if val == cls:
                return key
        raise KeyError(cls)
