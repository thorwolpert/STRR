# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
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
