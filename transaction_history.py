from transaction_record import TransactionRecord


class TransactionHistory:
    def __init__(self):
        self._transactions = []

    def append(self, transaction):
        if not isinstance(transaction, TransactionRecord):
            raise TypeError("transaction must be an instance of transactionRecord")

        self._transactions.append(transaction)

    def snapshot(self):
        return tuple(self._transactions)

    def __len__(self):
        return len(self._transactions)

    def __str__(self):
        return "\n".join([str(transaction) for transaction in self._transactions])