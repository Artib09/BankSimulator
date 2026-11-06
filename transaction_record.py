import datetime


class TransactionRecord:
    def __init__(self, transaction_type: str, amount: int, description: str, balance_after: int):
        self.type = transaction_type
        self.amount = amount
        self.balance = balance_after
        self.description = description
        self.time = datetime.datetime.now()

    def __str__(self):
        return str(self.__dict__)