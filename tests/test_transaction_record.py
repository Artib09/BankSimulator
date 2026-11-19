import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime

from transaction_record import TransactionRecord


class TransactionRecordTests(unittest.TestCase):
    def test_constructor(self) -> None:
        timestamp = datetime(2026, 11, 19, 12, 0)

        record = TransactionRecord(
            id=7,
            transaction_type="deposit",
            amount=1500,
            description="Initial deposit",
            balance_after=1500,
            time=timestamp,
        )

        self.assertEqual(record.id, 7)
        self.assertEqual(record.transaction_type, "deposit")
        self.assertEqual(record.amount, 1500)
        self.assertEqual(record.description, "Initial deposit")
        self.assertEqual(record.balance_after, 1500)
        self.assertEqual(record.time, timestamp)

    def test_fields_cannot_be_reassigned(self) -> None:
        record = TransactionRecord(
            id=1,
            transaction_type="deposit",
            amount=100,
            description="Test",
            balance_after=100,
        )

        with self.assertRaises(FrozenInstanceError):
            record.amount = 999

        self.assertEqual(record.amount, 100)

    def test_string_representation_contains_correct_data(self) -> None:
        record = TransactionRecord(
            id=7,
            transaction_type="deposit",
            amount=1500,
            description="Example description",
            balance_after=2500,
        )

        text = str(record)

        self.assertIn("deposit", text)
        self.assertIn("Example description", text)
        self.assertIn("1500", text)
        self.assertIn("2500", text)


if __name__ == "__main__":
    unittest.main()