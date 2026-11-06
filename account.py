from transaction_record import TransactionRecord
from transaction_history import TransactionHistory


class Account:
    _id_counter = 0

    def __init__(self, name):
        self._balance = 0
        self._history = TransactionHistory()
        self._id = Account._id_counter
        Account._id_counter += 1
        self.owner = name

    @property
    def balance(self):
        return self._balance

    @property
    def history(self):
        return self._history.snapshot()

    @staticmethod
    def _validate_amount(amount, balance=-1):
        if type(amount) is not int:
            raise TypeError("amount must be an integer number")

        if amount <= 0:
            raise ValueError("amount must be greater than zero")

        if balance != -1 and amount > balance:
            raise ValueError("insufficient funds")

    def _validate_recipient(self, recipient):
        if not isinstance(recipient, Account):
            raise TypeError("recipient must be an account")

        if recipient is self:
            raise ValueError("cannot transfer to the same account")

    @staticmethod
    def _validate_description(description: str):
        if not isinstance(description, str):
            raise TypeError("description must be a string")

    def withdraw(self, amount: int, description: str):
        self._validate_amount(amount, self._balance)
        self._validate_description(description)

        new_balance = self._balance - amount

        self._history.append(
            TransactionRecord(
                "withdraw",
                amount,
                description,
                new_balance))

        self._balance = new_balance

    def deposit(self, amount: int, description: str):
        self._validate_amount(amount)
        self._validate_description(description)

        new_balance = self._balance + amount

        self._history.append(
            TransactionRecord(
                "deposit",
                amount,
                description,
                new_balance))

        self._balance = new_balance

    def transfer(self, amount, recipient, description):
        # validation
        self._validate_amount(amount, self._balance)
        self._validate_recipient(recipient)
        self._validate_description(description)

        # data preparation
        sender_balance = self._balance - amount
        recipient_balance = recipient._balance + amount

        sender_record = TransactionRecord(
            "transfer_out",
            amount,
            description,
            sender_balance)

        recipient_record = TransactionRecord(
            "transfer_in",
            amount,
            description,
            recipient_balance)

        # transfer execution
        self._history.append(sender_record)
        recipient._history.append(recipient_record)

        self._balance = sender_balance
        recipient._balance = recipient_balance
