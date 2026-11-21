from account import Account
from transaction_record import TransactionRecord
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
    try:
        account_alex = Account("Alex")
        print(account_alex.balance)
        account_alex.deposit(100, "depo alex")
        print(account_alex.balance)
        account_alex.withdraw(90, "wdr alex")
        print(account_alex.balance)

        account_tom = Account("Tom")
        print(account_tom.balance)
        account_tom.deposit(1111, "depo tom")
        print(account_tom.balance)
        account_tom.withdraw(90, "wdr tom")
        print(account_tom.balance)

        account_tom.transfer(300, account_alex, "buy sth")
        print(account_tom.balance)
        print(account_alex.balance)

        trans = TransactionRecord(3, "some type", 15, "dsc", 1555)
        print(trans)

        print("\n \n history Alex")
        for record in account_alex.history:
            print(record)

    except ValueError as ex:
        print(ex)

if __name__ == "__main__":
    configure_logging()
    main()