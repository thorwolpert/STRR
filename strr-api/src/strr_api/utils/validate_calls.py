import functools
import inspect
from typing import Any, Optional


def validate_mutex(*mutex_args: str, min_count: int = 0, max_count: int = 1):
    """
    Validates that a specific subset of arguments adheres to mutual exclusivity rules.

    :param mutex_args: The names of the arguments to check.
    :param min_count: Minimum number of non-None values required.
    :param max_count: Maximum number of non-None values allowed.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Bind arguments to the function signature to handle args/kwargs mapping
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()  # Ensure we see default values (like None)

            # 2. Count how many of the watched arguments are not None
            active_count = sum(
                1 for name in mutex_args if name in bound.arguments and bound.arguments[name] is not None
            )

            # 3. Validation Logic
            if active_count > max_count:
                raise ValueError(
                    f"Too many arguments provided. Allowed max: {max_count}, "
                    f"Found: {active_count} ({', '.join(mutex_args)})"
                )

            if active_count < min_count:
                raise ValueError(
                    f"Not enough arguments provided. Required min: {min_count}, "
                    f"Found: {active_count} ({', '.join(mutex_args)})"
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
