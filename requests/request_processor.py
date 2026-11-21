"""Execute client requests using existing bank accounts."""

from account import Account
from .client_request import ClientRequest


class RequestProcessor:
    """Find the requested account and execute an operation."""

    def __init__(self, accounts: dict[int, Account]) -> None:
        self._accounts = accounts

    def process(self, request: ClientRequest) -> None:
        """Execute one request without duplicating account validation."""

        account = self._accounts.get(request.account_id)

        if account is None:
            raise ValueError(
                f"Unknown account: {request.account_id}"
            )

        if request.operation == "deposit":
            account.deposit(request.amount, request.description)
        elif request.operation == "withdraw":
            account.withdraw(request.amount, request.description)
        else:
            raise ValueError(
                f"Unsupported operation: {request.operation}"
            )