# Copyright 2024 Ole Kliemann
# SPDX-License-Identifier: MIT


class ResultException(Exception):
    def __init__(self, payload):
        self.payload = payload


class BaseResult:
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return f'Ok{self._value}'

    def __str__(self):
        return self.__repr__()

    def __eq__(lhs, rhs):
        return type(lhs) is type(rhs) and lhs._value == rhs._value

    def __hash__(self):
        return hash((self.__class__, self._value))

    def _unexpected(self, msg=None):
        raise AssertionError(f'{self.__str__()}' + (f': {msg}' if msg else ''))


class Ok(BaseResult):
    def __init__(self, value):
        super().__init__(value)

    def is_ok(self):
        return True

    def is_err(self):
        return False

    def expect(self, msg):
        return self._value

    def unwrap(self):
        return self._value

    def expect_err(self, msg):
        self._unexpected(msg)

    def unwrap_err(self):
        self._unexpected()

    def unwrap_or(self, alternative):
        return self._value

    def unwrap_or_return(self):
        return self._value


class Err(BaseResult):
    def __init__(self, value):
        super().__init__(value)

    def is_ok(self):
        return False

    def is_err(self):
        return True

    def expect(self, msg):
        self._unexpected(msg)

    def unwrap(self):
        self._unexpected()

    def expect_err(self, msg):
        return self._value

    def unwrap_err(self):
        return self._value

    def unwrap_or(self, alternative):
        return alternative

    def unwrap_or_return(self):
        raise ResultException(self._value)


def returns_result(*exceptions_to_catch):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                match e:
                    case AssertionError():
                        raise
                    case ResultException():
                        return Err(e.payload)
                    case _ if isinstance(e, exceptions_to_catch):
                        return Err(e)
                    case _:
                        new_exc = AssertionError(f'Unhandled exception: {str(e)}')
                        new_exc = new_exc.with_traceback(e.__traceback__)
                        raise new_exc from None

        return wrapper

    return decorator
