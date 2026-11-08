from account import Account
from transaction_record import TransactionRecord


def main():
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
        print(account_alex.history)
        print("\n \n history Tom")
        print(account_tom.history)

    except ValueError as ex:
        print(ex)

if __name__ == '__main__':
    main()