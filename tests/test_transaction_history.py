import unittest
from datetime import datetime

from transaction_history import TransactionHistory
from transaction_record import TransactionRecord


class TransactionHistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.history = TransactionHistory()

        self.first = TransactionRecord(
            id=1,
            transaction_type="deposit",
            amount=1000,
            description="First operation",
            balance_after=1000,
            time=datetime(2026, 11, 19, 12, 0),
        )

        self.second = TransactionRecord(
            id=2,
            transaction_type="withdraw",
            amount=200,
            description="Second operation",
            balance_after=800,
            time=datetime(2026, 11, 19, 12, 1),
        )

    def test_new_history_is_empty(self) -> None:
        self.assertEqual(len(self.history), 0)
        self.assertEqual(self.history.snapshot(), ())
        self.assertEqual(str(self.history), "")

    def test_append_preserves_order(self) -> None:
        self.history.append(self.first)
        self.history.append(self.second)

        self.assertEqual(len(self.history), 2)
        self.assertEqual(
            self.history.snapshot(),
            (self.first, self.second),
        )

    def test_invalid_records_are_rejected(self) -> None:
        self.history.append(self.first)
        before = self.history.snapshot()

        for value in (None, "transaction", 123, {}, []):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    self.history.append(value)

                self.assertEqual(self.history.snapshot(), before)

    def test_snapshot_does_not_change_after_append(self) -> None:
        self.history.append(self.first)
        snapshot = self.history.snapshot()

        self.history.append(self.second)

        self.assertIsInstance(snapshot, tuple)
        self.assertEqual(snapshot, (self.first,))
        self.assertEqual(
            self.history.snapshot(),
            (self.first, self.second),
        )


if __name__ == "__main__":
    unittest.main()