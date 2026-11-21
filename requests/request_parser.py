"""Parse client requests stored in a CSV file."""

import csv
from pathlib import Path
from typing import Iterator

from .client_request import ClientRequest


class RequestParser:
    """Read and validate client requests from a CSV file."""

    _EXPECTED_COLUMNS = {
        "request_id",
        "client_id",
        "account_id",
        "operation",
        "amount",
        "description",
    }

    _SUPPORTED_OPERATIONS = {"deposit", "withdraw"}

    def __init__(self, file_name: str | Path) -> None:
        self._file_name = Path(file_name)

    def parse(self) -> Iterator[ClientRequest]:
        """Yield valid requests from the CSV file.

        Raises:
            ValueError: If the file has an invalid header or a row
                contains invalid request data.
        """

        with self._file_name.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as csv_file:
            reader = csv.DictReader(csv_file)

            if reader.fieldnames is None:
                raise ValueError(
                    f"CSV file is empty: {self._file_name}"
                )

            missing_columns = (
                self._EXPECTED_COLUMNS - set(reader.fieldnames)
            )

            if missing_columns:
                raise ValueError(
                    "Missing CSV columns: "
                    f"{', '.join(sorted(missing_columns))}"
                )

            for row_number, row in enumerate(reader, start=2):
                yield self._parse_row(row, row_number)

    def _parse_row(
        self,
        row: dict[str, str],
        row_number: int,
    ) -> ClientRequest:
        """Convert one CSV row into a client request."""

        if None in row or any(value is None for value in row.values()):
            raise ValueError(
                f"Invalid number of fields in row {row_number}"
            )

        try:
            account_id = int(row["account_id"])
            amount = int(row["amount"])
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Invalid numeric value in row {row_number}: {error}"
            ) from error

        operation = row["operation"].strip().lower()

        if operation not in self._SUPPORTED_OPERATIONS:
            raise ValueError(
                f"Unsupported operation '{operation}' in row {row_number}. "
                f"Supported operations: "
                f"{', '.join(sorted(self._SUPPORTED_OPERATIONS))}"
            )

        return ClientRequest(
            request_id=row["request_id"].strip(),
            client_id=row["client_id"].strip(),
            account_id=account_id,
            operation=operation,
            amount=amount,
            description=row["description"].strip(),
        )