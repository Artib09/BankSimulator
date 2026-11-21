import logging
import unittest
from unittest.mock import patch

from decorators import (
    log_account_operation,
    log_operation,
    measure_time,
)


class LogOperationTests(unittest.TestCase):
    def test_preserves_result(self) -> None:
        @log_operation
        def add(first: int, second: int) -> int:
            return first + second

        self.assertEqual(add(2, 3), 5)

    def test_reraises_exception(self) -> None:
        @log_operation
        def fail() -> None:
            raise ValueError("invalid value")

        with self.assertRaises(ValueError):
            fail()

    def test_preserves_name(self) -> None:
        @log_operation
        def calculate_total() -> None:
            """Calculate total."""

        self.assertEqual(calculate_total.__name__, "calculate_total")
        self.assertEqual(calculate_total.__doc__, "Calculate total.")


class MeasureTimeTests(unittest.TestCase):
    def test_preserves_result(self) -> None:
        @measure_time()
        def multiply(first: int, second: int) -> int:
            return first * second

        self.assertEqual(multiply(3, 4), 12)

    def test_reraises_exception(self) -> None:
        @measure_time()
        def fail() -> None:
            raise ValueError("invalid value")

        with self.assertRaises(ValueError):
            fail()


class LogAccountOperationTests(unittest.TestCase):
    def test_uses_account_id(self) -> None:
        class FakeAccount:
            id = 42

            @log_account_operation
            def deposit(self, amount: int) -> int:
                return amount

        account = FakeAccount()

        with self.assertLogs("decorators", level="INFO") as logs:
            result = account.deposit(100)

        self.assertEqual(result, 100)
        self.assertIn("account_id=42", "\n".join(logs.output))


if __name__ == "__main__":
    unittest.main()