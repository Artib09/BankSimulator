from __future__ import annotations
from transaction_record import TransactionRecord

class HistoryIterator:
    """Iterate over a snapshot of transaction history."""
    def __init__(self, snapshot: tuple[TransactionRecord, ...]) -> None:
        self._history: tuple[TransactionRecord, ...] = snapshot
        self._pos: int = 0

    def __iter__(self) -> HistoryIterator:
        return self

    def __next__(self) -> TransactionRecord:
        if self._pos >= len(self._history):
            raise StopIteration

        transaction = self._history[self._pos]
        self._pos += 1
        return transaction
