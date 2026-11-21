from account import Account
from requests.request_parser import RequestParser
from requests.request_processor import RequestProcessor

import logging
from pathlib import Path


def configure_logging() -> None:
    """Configure console and file logging."""

    logs_directory = Path(__file__).resolve().parent / "logs"
    logs_directory.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(threadName)s | %(message)s"
        ),
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                logs_directory / "bank_simulator.log",
                encoding="utf-8",
                mode="w",
            ),
        ],
    )

def main() -> None:
    logging.info("Starting bank simulation")

    account_alex = Account("Alex")
    account_tom = Account("Tom")

    accounts = {
        account_alex.id: account_alex,
        account_tom.id: account_tom,
    }

    for account in accounts.values():
        print(f"Account {account.id}: {account.owner}")

    parser = RequestParser(
        Path(__file__).resolve().parent / "data" / "requests.csv"
    )
    processor = RequestProcessor(accounts)

    try:
        for request in parser.parse():
            try:
                processor.process(request)
            except ValueError as error:
                logging.warning(
                    "Rejected request=%s | %s",
                    request.request_id,
                    error,
                )
            else:
                logging.info(
                    "Completed request=%s",
                    request.request_id,
                )
    except (OSError, ValueError) as error:
        logging.error("Cannot finish reading requests: %s", error)

    for account in accounts.values():
        print(f"\n{account.owner}: balance={account.balance}")

        for transaction in account.history:
            print(transaction)

if __name__ == "__main__":
    configure_logging()
    main()