from transaction_record import TransactionRecord


class TransactionHistory:
    """Transaction storage synchronized by its owning account."""
    def __init__(self) -> None:
        self._transactions: list[TransactionRecord] = []

    def append(self, transaction: TransactionRecord) -> None:
        if not isinstance(transaction, TransactionRecord):
            raise TypeError("transaction must be an instance of TransactionRecord")

        self._transactions.append(transaction)

    def snapshot(self) -> tuple[TransactionRecord, ...]:
        return tuple(self._transactions)

    def __len__(self):
        return len(self._transactions)

    def __str__(self):
        return "\n".join(
            str(transaction)
            for transaction in self._transactions
        )