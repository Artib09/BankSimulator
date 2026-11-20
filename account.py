from __future__ import annotations
from logging import measure_time

from threading import Lock
from typing import ClassVar

from transaction_record import TransactionRecord
from transaction_history import TransactionHistory


class Account:
    """Bank account with synchronized balance and transaction history. Stores account balance as amount of grosze as integer."""
    _id_counter: ClassVar[int] = 0
    _transactions_id_counter: ClassVar[int] = 0
    _counter_lock = Lock()

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        if not name.strip():
            raise ValueError("name cannot be empty")

        self._lock = Lock()
        self._balance: int = 0
        self._history = TransactionHistory()
        self.owner: str = name

        with Account._counter_lock:
            self._id: int = Account._id_counter
            Account._id_counter += 1

    @property
    def id(self) -> int:
        return self._id

    @property
    def balance(self) -> int:
        with self._lock:
            return self._balance

    @property
    def history(self) -> tuple[TransactionRecord, ...]:
        with self._lock:
            return self._history.snapshot()

    @staticmethod
    def _next_transaction_id() -> int:
        with Account._counter_lock:
            transaction_id = Account._transactions_id_counter
            Account._transactions_id_counter += 1
            return transaction_id

    @staticmethod
    def _validate_amount(amount: int) -> None:
        if type(amount) is not int:
            raise TypeError("amount must be an integer number of cents")

        if amount <= 0:
            raise ValueError("amount must be greater than zero")

    @staticmethod
    def _validate_description(description: str) -> None:
        if not isinstance(description, str):
            raise TypeError("description must be a string")

    def _validate_recipient(self, recipient: Account) -> None:
        if not isinstance(recipient, Account):
            raise TypeError("recipient must be an account")

        if recipient is self:
            raise ValueError("cannot transfer to the same account")

    def _ensure_sufficient_funds(self, amount: int) -> None:
        """Must be called while holding this account's lock."""
        if amount > self._balance:
            raise ValueError("insufficient funds")

    @measure_time
    def withdraw(self, amount: int, description: str) -> None:
        self._validate_amount(amount)
        self._validate_description(description)

        with self._lock:
            self._ensure_sufficient_funds(amount)

            new_balance: int = self._balance - amount

            record = TransactionRecord(
                id = self._next_transaction_id(),
                transaction_type = "withdraw",
                amount = amount,
                description = description,
                balance_after = new_balance
            )

            self._history.append(record)
            self._balance = new_balance

    @measure_time
    def deposit(self, amount: int, description: str) -> None:
        self._validate_amount(amount)
        self._validate_description(description)

        with self._lock:
            new_balance = self._balance + amount

            record = TransactionRecord(
                id = self._next_transaction_id(),
                transaction_type = "deposit",
                amount = amount,
                description = description,
                balance_after = new_balance
            )

            self._history.append(record)
            self._balance = new_balance

    @measure_time
    def transfer(self, amount: int, recipient: Account, description: str) -> None:
        # validation
        self._validate_amount(amount)
        self._validate_recipient(recipient)
        self._validate_description(description)

        #solution for a potential thread deadlock
        first, second = sorted(
            (self, recipient),
            key = lambda account: account._id)

        with first._lock:
            with second._lock:
                self._ensure_sufficient_funds(amount)

                # data preparation
                transaction_id = self._next_transaction_id()
                sender_balance = self._balance - amount
                recipient_balance = recipient._balance + amount

                sender_record = TransactionRecord(
                    id = transaction_id,
                    transaction_type = "transfer_out",
                    amount = amount,
                    description = description,
                    balance_after = sender_balance
                )

                recipient_record = TransactionRecord(
                    id = transaction_id,
                    transaction_type = "transfer_in",
                    amount = amount,
                    description = description,
                    balance_after = recipient_balance
                )

                # transfer execution
                self._history.append(sender_record)
                recipient._history.append(recipient_record)

                self._balance = sender_balance
                recipient._balance = recipient_balance