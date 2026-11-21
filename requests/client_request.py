"""Immutable client request loaded from a CSV file."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClientRequest:
    """A single operation requested by a bank client."""

    request_id: str
    client_id: str
    account_id: int
    operation: str
    amount: int
    description: str