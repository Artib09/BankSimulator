from account import Account
from requests.request_parser import RequestParser
from requests.request_processor import RequestProcessor

import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat


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

def process_file(
    file_path: Path,
    processor: RequestProcessor,
) -> None:
    """Read and process requests from one client file."""

    logging.info("Reading requests: %s", file_path.name)

    parser = RequestParser(file_path)

    try:
        for request in parser.parse():
            try:
                processor.process(request)
            except ValueError as error:
                logging.warning(
                    "Rejected request=%s | account_id=%s | %s",
                    request.request_id,
                    request.account_id,
                    error,
                )
            else:
                logging.info(
                    "Completed request=%s",
                    request.request_id,
                )
    except (OSError, ValueError) as error:
        logging.error(
            "Cannot finish reading %s | %s",
            file_path.name,
            error,
        )
    else:
        logging.info(
            "Finished processing file: %s",
            file_path.name,
        )

def main() -> None:
    logging.info("Starting bank simulation")

    account_alex = Account("Alex")
    account_tom = Account("Tom")

    accounts = {
        account_alex.id: account_alex,
        account_tom.id: account_tom,
    }

    processor = RequestProcessor(accounts)

    data_directory = Path(__file__).resolve().parent / "data"
    request_files = (
        data_directory / "alex_account.csv",
        data_directory / "tom_account.csv",
    )

    for file_path in request_files:
        if not file_path.is_file():
            logging.error("Request file does not exist: %s", file_path)
            return

    with ThreadPoolExecutor(
            max_workers=2,
            thread_name_prefix="client",
    ) as executor:
        results = executor.map(
            process_file,
            request_files,
            repeat(processor),
        )

        for _ in results:
            pass

    for account in accounts.values():
        print(f"\n{account.owner}: balance={account.balance}")

        for transaction in account.history:
            print(transaction)

    logging.info("Bank simulation finished")


if __name__ == "__main__":
    configure_logging()
    main()