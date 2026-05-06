from __future__ import annotations

from typing import Callable, TypeVar, cast

import allure

F = TypeVar("F", bound=Callable[..., object])


def allure_step(step_name: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        return cast(F, allure.step(step_name)(func))

    return decorator
