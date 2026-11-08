import datetime


class TransactionRecord:
    id: int
    type: str
    amount: int
    description: str
    balance_after: int
    time: datetime.datetime

    def __init__(self, id: int, transaction_type: str, amount: int, description: str, balance_after: int):
        self.id = id
        self.type = transaction_type
        self.amount = amount
        self.description = description
        self.balance_after = balance_after
        self.time = datetime.datetime.now()

    def __str__(self):
        return str(self.__dict__)