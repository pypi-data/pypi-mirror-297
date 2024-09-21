"""Exceptions for MySpeed API Python client."""


class MySpeedAPIError(Exception):
    """Exception to indicate a general API error."""

    pass


class MySpeedAPIConnectionError(MySpeedAPIError):
    """Exception to indicate a communication error."""

    pass


class MySpeedAPIAuthenticationError(MySpeedAPIError):
    """Exception to indicate an authentication error."""

    pass


class MySpeedAPIJSONDecodeError(MySpeedAPIError):
    """Exception to indicate a JSON decode error."""

    pass


__all__ = [
    "MySpeedAPIError",
    "MySpeedAPIConnectionError",
    "MySpeedAPIAuthenticationError",
    "MySpeedAPIJSONDecodeError",
]
