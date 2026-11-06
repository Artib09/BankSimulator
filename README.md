# Python Banking Simulator

An educational project that simulates a simplified banking system,
including bank accounts, transaction histories, and a queue of client
requests.

The project aims to demonstrate advanced Python concepts through
practical use of decorators, iterators, generators, regular expressions,
threading, and multiprocessing.

## Project Status

**In development.**

The current implementation provides a basic account model, deposit,
withdrawal, and transfer operations, and transaction history recording.

Upcoming work focuses on stronger validation, unit testing, thread-safe
account operations, and report generation.

## Core Design

- Monetary amounts are stored as integers representing grosze
  (1 PLN = 100 grosze).
- Each account has an owner, an identifier, a balance, and a transaction
  history.
- Transaction records contain the operation type, amount, description,
  timestamp, and balance after the operation.
- Transfers are recorded in both the sender's and the recipient's
  transaction histories.

## Planned Features

- Input validation and sufficient-funds checks.
- Authorization and operation logging using custom decorators.
- Multithreaded simulation of concurrent clients.
- A request queue and synchronized access to accounts.
- A custom iterator for transaction histories.
- Generators for filtering and processing transactions.
- Rule-based flagging of potentially suspicious transactions using
  regular expressions.
- Parallel report computation using multiprocessing.
- Performance comparisons between sequential, threaded, and
  process-based execution, with an analysis of the Global Interpreter
  Lock (GIL).
- Unit tests and concurrency tests.

## Current Project Structure

- `account.py` — account model and deposit, withdrawal, and transfer
  operations.
- `transaction_record.py` — individual transaction records.
- `transaction_history.py` — transaction history storage.
- `main.py` — an example application scenario.

The structure will evolve as additional features are implemented.

## Requirements

- Python 3.12 or newer.
- The current implementation uses only the Python standard library.

## Running the Application

Run the example scenario from the repository's root directory:

    python main.py

## Educational Purpose

This project is being developed for an Advanced Python Programming
course. It explores transaction modeling, shared-state synchronization,
and concurrent and parallel data processing.

It is an educational simulator, not a production banking system,
and must not be used to manage real funds.