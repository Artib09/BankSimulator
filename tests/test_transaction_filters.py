import unittest

from transaction_filters import (
    filter_by_type,
    filter_less_than_amount,
    filter_more_than_amount,
)
from transaction_record import TransactionRecord


class TransactionFiltersTests(unittest.TestCase):
    def setUp(self) -> None:
        self.deposit = TransactionRecord(
            id=1,
            transaction_type="deposit",
            amount=20_000,
            description="Initial deposit",
            balance_after=20_000,
        )

        self.small_withdrawal = TransactionRecord(
            id=2,
            transaction_type="withdraw",
            amount=5000,
            description="Small withdrawal",
            balance_after=15_000,
        )

        self.large_withdrawal = TransactionRecord(
            id=3,
            transaction_type="withdraw",
            amount=10_000,
            description="Large withdrawal",
            balance_after=5000,
        )

        self.transactions = (
            self.deposit,
            self.small_withdrawal,
            self.large_withdrawal,
        )

    def test_filter_by_type(self) -> None:
        result = filter_by_type(self.transactions, "withdraw")

        self.assertEqual(
            list(result),
            [self.small_withdrawal, self.large_withdrawal],
        )

    def test_filter_less_than_amount_excludes_threshold(self) -> None:
        result = filter_less_than_amount(self.transactions, 10_000)

        self.assertEqual(list(result), [self.small_withdrawal])

    def test_filter_more_than_amount_excludes_threshold(self) -> None:
        result = filter_more_than_amount(self.transactions, 10_000)

        self.assertEqual(list(result), [self.deposit])

    def test_filters_return_no_results_when_nothing_matches(self) -> None:
        self.assertEqual(
            list(filter_by_type(self.transactions, "transfer_out")),
            [],
        )
        self.assertEqual(
            list(filter_less_than_amount(self.transactions, 5000)),
            [],
        )
        self.assertEqual(
            list(filter_more_than_amount(self.transactions, 20_000)),
            [],
        )

    def test_filters_accept_empty_input(self) -> None:
        self.assertEqual(list(filter_by_type((), "withdraw")), [])
        self.assertEqual(list(filter_less_than_amount((), 10_000)), [])
        self.assertEqual(list(filter_more_than_amount((), 10_000)), [])

    def test_filters_can_be_combined(self) -> None:
        withdrawals = filter_by_type(self.transactions, "withdraw")
        above_lower_limit = filter_more_than_amount(withdrawals, 5000)
        result = filter_less_than_amount(above_lower_limit, 15_000)

        self.assertEqual(list(result), [self.large_withdrawal])


if __name__ == "__main__":
    unittest.main()