from collections.abc import Iterable, Iterator
from email.utils import decode_rfc2231

from transaction_record import TransactionRecord

def filter_by_type(transactions: Iterable[TransactionRecord], transaction_type: str) -> Iterator[TransactionRecord]:
    for transaction in transactions:
        if transaction.transaction_type == transaction_type:
            yield transaction

def filter_less_than_amount(transactions: Iterable[TransactionRecord], amount: int) -> Iterator[TransactionRecord]:
    for transaction in transactions:
        if transaction.amount < amount:
            yield transaction

def filter_more_than_amount(transactions: Iterable[TransactionRecord], amount: int) -> Iterator[TransactionRecord]:
    for transaction in transactions:
        if transaction.amount > amount:
            yield transaction

def filter_by_amount_in_range(transactions: Iterable[TransactionRecord], start: int, stop: int) -> Iterator[TransactionRecord]:
    more_than_amount = filter_more_than_amount(transactions, start)
    return filter_less_than_amount(more_than_amount, stop)