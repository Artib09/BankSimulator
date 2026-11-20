import unittest

from history_iterator import HistoryIterator
from transaction_record import TransactionRecord


class HistoryIteratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.first = TransactionRecord(
            id=1,
            transaction_type="deposit",
            amount=1000,
            description="Initial deposit",
            balance_after=1000,
        )

        self.second = TransactionRecord(
            id=2,
            transaction_type="withdraw",
            amount=200,
            description="ATM withdrawal",
            balance_after=800,
        )

    def test_returns_records_in_order_and_stops(self) -> None:
        iterator = HistoryIterator((self.first, self.second))

        self.assertEqual(next(iterator), self.first)
        self.assertEqual(next(iterator), self.second)

        with self.assertRaises(StopIteration):
            next(iterator)

    def test_empty_history(self) -> None:
        iterator = HistoryIterator(())

        self.assertEqual(list(iterator), [])

    def test_iter_returns_self_without_resetting_position(self) -> None:
        iterator = HistoryIterator((self.first, self.second))
        next(iterator)

        self.assertIs(iter(iterator), iterator)
        self.assertEqual(list(iterator), [self.second])


if __name__ == "__main__":
    unittest.main()