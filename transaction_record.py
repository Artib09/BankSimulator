from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class TransactionRecord:
    """Immutable record of one completed transaction."""

    id: int
    transaction_type: str
    amount: int
    description: str
    balance_after: int
    time: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return str(self.__dict__)