from typing import Any


def with_callback(
    max_tries: int,
    begin_callback: callable,
    end_callback: callable,
):
    def outer_wrapper(target_func):
        def inner_wrapper(instance: Any, arg1: str, arg2: int):
            begin_callback()
            for _ in range(max_tries):
                result = target_func(instance, arg1, arg2)
            end_callback()

        return inner_wrapper

    return outer_wrapper
