from typing import Any, Union

from ._resolver import AnyClass, Resolver

__all__ = ("Packable",)


class Packable:
    """
    Registers classes to be packable by associating them with a resolver.

    This class acts as a decorator or direct registrar for classes to
    ensure that they can be packed and unpacked correctly by the system.
    """

    def __init__(self, resolver: Resolver) -> None:
        """
        Initialize a `Packable` instance with the given resolver.

        :param resolver: The resolver used to manage class registration.
        """
        self._resolver = resolver

    def __call__(self, cls_or_name: Union[str, AnyClass]) -> Any:
        """
        Register a class with the resolver, optionally with a custom name.

        If a class is passed, it will be registered directly. If a string is
        passed, it will be used as a custom name for the class during registration.

        :param cls_or_name: The class or name to register with the resolver.
        :return: The registered class or a decorator if a name is provided.
        """
        if not isinstance(cls_or_name, str):
            self._resolver.register(cls=cls_or_name)
            return cls_or_name

        def wrapped(cls: AnyClass) -> AnyClass:
            """
            Register the class with a custom name.

            :param cls: The class to be registered.
            :return: The class after registration.
            """
            self._resolver.register(cls=cls, name=cls_or_name)
            return cls

        return wrapped
