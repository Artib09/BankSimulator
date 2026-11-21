# Bank Simulator

An educational banking simulator written in Python. The project demonstrates account operations, immutable transaction records, generators, decorators, CSV processing, and concurrent execution using threads.

Amounts are stored as integers representing the smallest currency unit. Floating-point values are not used for account balances.

## Features

- Account creation with automatically generated identifiers.
- Deposits, withdrawals, and transfers.
- Validation of operation amounts and descriptions.
- Rejection of withdrawals and transfers when funds are insufficient.
- Immutable transaction records.
- Transaction history snapshots.
- Generator-based transaction filters.
- CSV-based client requests.
- Concurrent processing of client request files.
- Console and file logging.
- Unit tests for the core components.

## Requirements

- Python 3.12 or newer.
- No third-party packages are currently required.

The application uses the Python standard library.

## Project Structure

```text
.
├── data/
│   ├── Alex_account.csv
│   └── tom_account.csv
├── logs/
│   └── bank_simulator.log
├── requests/
│   ├── __init__.py
│   ├── client_request.py
│   ├── request_parser.py
│   └── request_processor.py
├── tests/
│   ├── test_account.py
│   ├── test_decorators.py
│   ├── test_history_iterator.py
│   ├── test_transaction_filters.py
│   ├── test_transaction_history.py
│   └── test_transaction_record.py
├── account.py
├── account_repository.py
├── decorators.py
├── history_iterator.py
├── main.py
├── transaction_filters.py
├── transaction_history.py
├── transaction_record.py
└── README.md
```

The `logs/` directory is created automatically if it does not exist.

`account_repository.py` is not used by the current application entry point. Accounts are passed to the request processor in a dictionary indexed by account identifier.

## Running the Application

Run the application from the project root:

```bash
python main.py
```

The application:

1. Configures console and file logging.
2. Creates accounts for Alex and Tom.
3. Registers the accounts in a dictionary.
4. Processes the two explicitly selected CSV files using a thread pool.
5. Prints final balances and transaction histories.

The configured input files are:

```text
data/Alex_account.csv
data/tom_account.csv
```

File names must match the paths defined in `main.py`.

Only these files are processed. Other CSV files in the directory are ignored.

## Client Request Format

Each CSV file must contain the following columns:

```csv
request_id,client_id,account_id,operation,amount,description
```

Example:

```csv
request_id,client_id,account_id,operation,amount,description
req-001,client-alex,0,deposit,10000,Initial deposit
req-002,client-alex,0,withdraw,2500,Shopping
```

| Field | Description |
|---|---|
| `request_id` | Identifier used to identify the request in logs |
| `client_id` | Client identifier supplied in the input data |
| `account_id` | Integer identifier of the account |
| `operation` | Supported operation: `deposit` or `withdraw` |
| `amount` | Integer amount in the smallest currency unit |
| `description` | Transaction description |

For example, `10000` represents 100.00 currency units.

### Account Identifiers

Account identifiers are assigned automatically, starting at `0`.

In a fresh application process, when Alex and Tom are the first accounts created:

- Alex receives account identifier `0`.
- Tom receives account identifier `1`.

The CSV data must reference the identifiers assigned to these accounts.

### Supported Request Operations

CSV requests currently support:

- `deposit`
- `withdraw`

Transfers are implemented in the account model but are not currently supported by the CSV request format.

## Request Processing

The request-processing flow is:

```text
CSV file
    ↓
RequestParser
    ↓
ClientRequest
    ↓
RequestProcessor
    ↓
Account.deposit() or Account.withdraw()
    ↓
Transaction history and logs
```

### Parser

`RequestParser` reads CSV records and yields `ClientRequest` objects.

It checks the input structure, converts numeric fields, and validates operation names. It does not build an intermediate list containing all requests.

### Processor

`RequestProcessor` finds the requested account and calls the appropriate account method.

It does not duplicate the financial validation already implemented in `Account`.

### Account

`Account` remains responsible for:

- Validating amounts and descriptions.
- Checking available funds.
- Updating balances.
- Creating transaction records.
- Protecting shared account state with locks.

## Concurrent Processing

The application uses `ThreadPoolExecutor` with up to two worker threads.

Each task reads and processes one client file. Requests within that file are executed sequentially.

The processor and account objects are shared between tasks.

Account balances and histories are protected by account-level locks. Shared identifier counters are protected by a separate lock.

Transfers acquire both account locks in account identifier order to avoid inconsistent lock ordering.

### Ordering

Request order is preserved within each file.

Execution order between different files is not guaranteed. As a result:

- Log messages may appear in different orders between runs.
- Transaction identifiers may be interleaved between accounts.
- Requests affecting the same account from different files may have order-dependent outcomes.

For the current demonstration, requests for each client account are kept in one file.

The small example dataset is intended to demonstrate concurrent execution, not to prove a performance improvement.

## Transaction History

Each completed operation produces an immutable `TransactionRecord`.

A record contains:

- Transaction identifier.
- Transaction type.
- Amount.
- Description.
- Balance after the operation.
- Creation time.

An account exposes its history as a tuple snapshot.

A transfer creates two records with a shared transaction identifier:

- `transfer_out` for the sender.
- `transfer_in` for the recipient.

Rejected operations do not create completed transaction records.

## Transaction Filters

The current filters are:

```python
filter_by_type(transactions, transaction_type)
filter_less_than_amount(transactions, amount)
filter_more_than_amount(transactions, amount)
filter_by_amount_in_range(transactions, start, stop)
```

The filters support lazy processing and can be combined into pipelines.

Amount comparisons are strict:

- `filter_less_than_amount()` uses `<`.
- `filter_more_than_amount()` uses `>`.
- `filter_by_amount_in_range()` excludes both boundaries.

Regex-based filtering has not been implemented.

## Decorators

The project contains three custom decorators:

| Decorator | Purpose | Current integration |
|---|---|---|
| `log_operation` | Logs function execution | Available for use; not applied in the current entry point |
| `measure_time(warning_threshold=...)` | Measures execution time and optionally logs a warning when a threshold is exceeded | Available for use; not applied in the current entry point |
| `log_account_operation` | Logs account operations using `self.id` | Applied to deposits, withdrawals, and transfers |

All three use `functools.wraps` to preserve the metadata of the decorated callable.

## Logging and Error Handling

Logs are written to:

- The console.
- `logs/bank_simulator.log`.

The log file is overwritten at application startup, so it contains messages from the current run only.

Log entries include:

- Timestamp.
- Severity level.
- Thread name.
- Message.

Expected request rejections, such as insufficient funds, are logged as warnings without a traceback.

Unexpected exceptions in decorated account operations are logged with a traceback and re-raised.

### Input Errors

A file-reading or parsing error stops processing of the affected file.

Previously completed operations are not rolled back.

An expected rejection of an individual request does not stop processing the remaining requests in that file.

## Running Tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

The existing test modules cover:

- Accounts.
- Transaction records.
- Transaction history.
- Transaction filters.
- The custom history iterator.
- Decorators.

Dedicated tests for CSV parsing, request processing, and concurrent access are still to be added.

The repository should be tested locally after changes; this README does not assert a specific test count or a verified passing result.

## Course Requirement Mapping

| Topic | Implementation | Status |
|---|---|---|
| Two custom function decorators | `decorators.py`: `log_operation`, `measure_time` | Implemented; practical integration remains |
| Parameterized decorator | `decorators.py`: `measure_time(warning_threshold=...)` | Implemented |
| Metadata preservation | `functools.wraps` in the custom decorators | Implemented |
| Custom method decorator using `self` | `decorators.py`: `log_account_operation` | Implemented and used |
| Built-in method decorator | `account.py`: `@staticmethod` | Implemented and used |
| Custom iterator | `history_iterator.py`: `HistoryIterator` | Implemented and tested; not used in the current application flow |
| Generator functions | Transaction filters and `RequestParser.parse()` | Implemented |
| Generator expressions | `TransactionHistory.__str__()` | Implemented |
| Logging | `main.py` and `decorators.py` | Implemented |
| Threads and synchronized shared state | `main.py`: `ThreadPoolExecutor`; `account.py`: `Lock` | Implemented |
| Unit tests | `tests/` | Implemented, but not for all classes|
| Regular expressions | Not implemented |
| CPU-bound processing with processes | Not implemented |
| Sequential, thread, and process benchmark | Not implemented |

