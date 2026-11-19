import unittest

from account import Account

class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.sender_acc = Account("Alex")
        self.receiver_acc = Account("Tom")

    def test_account_creation(self) -> None:
        self.assertEqual(self.sender_acc.owner, "Alex")
        self.assertEqual(self.sender_acc.balance, 0)
        self.assertEqual(self.sender_acc.history, ())

    def test_accounts_have_different_ids(self) -> None:
        self.assertNotEqual(self.sender_acc.id, self.receiver_acc.id)

    def test_invalid_owner(self) -> None:
        #invalid type
        for name in (None, 123, True, [], {}):
            with self.subTest(name=name):
                with self.assertRaises(TypeError):
                    Account(name)

        #empty text or whitespace
        for name in ("", " ", "\t", "\n", " \t\n "):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    Account(name)


    def test_deposit_updates_balance_and_history(self) -> None:
        self.sender_acc.deposit(1000, "Initial deposit")

        self.assertEqual(self.sender_acc.balance, 1000)
        self.assertEqual(len(self.sender_acc.history), 1)

        record = self.sender_acc.history[0]

        self.assertEqual(record.transaction_type, "deposit")
        self.assertEqual(record.amount, 1000)
        self.assertEqual(record.description, "Initial deposit")
        self.assertEqual(record.balance_after, 1000)


    def test_withdraw_updates_balance_and_history(self) -> None:
        self.sender_acc.deposit(1000, "Initial deposit")
        self.sender_acc.withdraw(300, "ATM withdrawal")

        self.assertEqual(self.sender_acc.balance, 700)
        self.assertEqual(len(self.sender_acc.history), 2)

        record = self.sender_acc.history[-1]

        self.assertEqual(record.transaction_type, "withdraw")
        self.assertEqual(record.amount, 300)
        self.assertEqual(record.description, "ATM withdrawal")
        self.assertEqual(record.balance_after, 700)

    def test_withdraw_entire_balance_allowed(self) -> None:
        self.sender_acc.deposit(1000, "Initial deposit")
        self.sender_acc.withdraw(1000, "Withdraw everything")

        self.assertEqual(self.sender_acc.balance, 0)
        self.assertEqual(self.sender_acc.history[-1].balance_after, 0)

    def test_insufficient_withdrawal_leaves_account_unchanged(self) -> None:
        self.sender_acc.deposit(100, "Initial deposit")
        before = (self.sender_acc.balance, self.sender_acc.history)

        with self.assertRaises(ValueError):
            self.sender_acc.withdraw(101, "Too much")

        self.assertEqual(
            (self.sender_acc.balance, self.sender_acc.history),
            before,
        )


    def test_transfer_updates_accounts_and_histories(self) -> None:
        self.sender_acc.deposit(1000, "Sender deposit")
        self.receiver_acc.deposit(200, "Recipient deposit")

        total_before = self.sender_acc.balance + self.receiver_acc.balance

        self.sender_acc.transfer(300, self.receiver_acc, "Payment")

        self.assertEqual(self.sender_acc.balance, 700)
        self.assertEqual(self.receiver_acc.balance, 500)
        self.assertEqual(
            self.sender_acc.balance + self.receiver_acc.balance,
            total_before,
        )
        self.assertEqual(len(self.sender_acc.history), 2)
        self.assertEqual(len(self.receiver_acc.history), 2)

        outgoing = self.sender_acc.history[-1]
        incoming = self.receiver_acc.history[-1]

        self.assertEqual(outgoing.id, incoming.id)

        self.assertEqual(outgoing.transaction_type, "transfer_out")
        self.assertEqual(incoming.transaction_type, "transfer_in")

        self.assertEqual(outgoing.amount, 300)
        self.assertEqual(incoming.amount, 300)

        self.assertEqual(outgoing.description, "Payment")
        self.assertEqual(incoming.description, "Payment")

        self.assertEqual(outgoing.balance_after, 700)
        self.assertEqual(incoming.balance_after, 500)

    def test_transferring_entire_balance_is_allowed(self) -> None:
        self.sender_acc.deposit(1000, "Initial deposit")

        self.sender_acc.transfer(1000, self.receiver_acc, "Everything")

        self.assertEqual(self.sender_acc.balance, 0)
        self.assertEqual(self.receiver_acc.balance, 1000)

    def test_rejected_transfers_leave_both_accounts_unchanged(self) -> None:
        self.sender_acc.deposit(1000, "Initial deposit")
        self.receiver_acc.deposit(200, "Initial deposit")

        cases = (
            (1001, self.receiver_acc, ValueError),
            (100, self.sender_acc, ValueError),
            (100, None, TypeError),
            (100, "Tom", TypeError),
        )

        for amount, receiver, expected_error in cases:
            with self.subTest(amount=amount, recipient=receiver):
                before = (
                    self.sender_acc.balance,
                    self.sender_acc.history,
                    self.receiver_acc.balance,
                    self.receiver_acc.history,
                )

                with self.assertRaises(expected_error):
                    self.sender_acc.transfer(amount, receiver, "Rejected")

                after = (
                    self.sender_acc.balance,
                    self.sender_acc.history,
                    self.receiver_acc.balance,
                    self.receiver_acc.history,
                )

                self.assertEqual(after, before)


    def test_invalid_amounts_are_rejected_all_operations(self) -> None:
        cases = (
            (0, ValueError),
            (-1, ValueError),
            (1.5, TypeError),
            ("100", TypeError),
            (True, TypeError),
            (False, TypeError),
            (None, TypeError),
        )

        self.sender_acc.deposit(1000, "Initial deposit")

        for operation in ("deposit", "withdraw", "transfer"):
            for amount, expected_error in cases:
                with self.subTest(operation=operation, amount=amount):
                    before = (
                        self.sender_acc.balance,
                        self.sender_acc.history,
                        self.receiver_acc.balance,
                        self.receiver_acc.history,
                    )

                    with self.assertRaises(expected_error):
                        if operation == "transfer":
                            self.sender_acc.transfer(
                                amount, self.receiver_acc, "Invalid amount"
                            )
                        else:
                            getattr(self.sender_acc, operation)(
                                amount, "Invalid amount"
                            )

                    after = (
                        self.sender_acc.balance,
                        self.sender_acc.history,
                        self.receiver_acc.balance,
                        self.receiver_acc.history,
                    )

                    self.assertEqual(after, before)

    def test_invalid_descriptions_accounts_unchanged(self) -> None:
        self.sender_acc.deposit(1000, "Initial deposit")

        for operation in ("deposit", "withdraw", "transfer"):
            for description in (None, 123, True, []):
                with self.subTest(
                        operation=operation,
                        description=description,
                ):
                    before = (
                        self.sender_acc.balance,
                        self.sender_acc.history,
                        self.receiver_acc.balance,
                        self.receiver_acc.history,
                    )

                    with self.assertRaises(TypeError):
                        if operation == "transfer":
                            self.sender_acc.transfer(
                                100, self.receiver_acc, description
                            )
                        else:
                            getattr(self.sender_acc, operation)(
                                100, description
                            )

                    after = (
                        self.sender_acc.balance,
                        self.sender_acc.history,
                        self.receiver_acc.balance,
                        self.receiver_acc.history,
                    )

                    self.assertEqual(after, before)

    def test_multiple_operations_history_balances(self) -> None:
        self.sender_acc.deposit(1000, "First deposit")
        self.sender_acc.deposit(500, "Second deposit")
        self.sender_acc.withdraw(200, "Withdrawal")

        history = self.sender_acc.history

        self.assertEqual(self.sender_acc.balance, 1300)
        self.assertEqual(
            [record.balance_after for record in history],
            [1000, 1500, 1300],
        )
        self.assertEqual(
            len({record.id for record in history}),
            len(history),
        )

    def test_history_is_a_snapshot(self) -> None:
        self.sender_acc.deposit(100, "First deposit")
        old_history = self.sender_acc.history

        self.sender_acc.deposit(200, "Second deposit")

        self.assertIsInstance(old_history, tuple)
        self.assertEqual(len(old_history), 1)
        self.assertEqual(old_history[0].balance_after, 100)
        self.assertEqual(len(self.sender_acc.history), 2)


if __name__ == "__main__":
    unittest.main()