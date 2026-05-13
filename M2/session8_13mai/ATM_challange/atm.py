# atm.py


import json

from bank_exceptions import (
    AccountNotFoundError,
    DuplicateAccountError,
    InvalidAmountError,
    InsufficientFundsError,
    SameAccountTransferError,
)

# JSON SAVE / LOAD

def save(accounts):
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)


def load():
    try:
        with open("accounts.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # prima rulare, fisierul nu exista inca

# DATA


accounts = load()   # incarca datele salvate


# HELPERS


def _require_account(name: str) -> None:
    """Raise AccountNotFoundError if the account doesn't exist."""
    if name not in accounts:
        raise AccountNotFoundError(f"Account '{name}' does not exist.")


def _require_positive_amount(amount: float) -> None:
    """Raise InvalidAmountError if the amount is not positive."""
    if amount <= 0:
        raise InvalidAmountError("Amount must be greater than 0.")



# BUSINESS LOGIC


def create_account(name: str) -> None:
    """Create a new account with 0 gold."""
    if not name:
        raise ValueError("Account name cannot be empty.")
    if name in accounts:
        raise DuplicateAccountError(f"Account '{name}' already exists.")
    accounts[name] = 0


def deposit(name: str, amount: float) -> None:
    """Add gold to an existing account."""
    _require_account(name)
    _require_positive_amount(amount)
    accounts[name] += amount


def withdraw(name: str, amount: float) -> None:
    """Remove gold from an existing account."""
    _require_account(name)
    _require_positive_amount(amount)
    if accounts[name] < amount:
        raise InsufficientFundsError(
            f"'{name}' only has {accounts[name]} gold. Cannot withdraw {amount}."
        )
    accounts[name] -= amount


def transfer(sender: str, receiver: str, amount: float) -> None:
    """Move gold from one account to another."""
    _require_account(sender)
    _require_account(receiver)
    if sender == receiver:
        raise SameAccountTransferError("Sender and receiver must be different accounts.")
    _require_positive_amount(amount)
    if accounts[sender] < amount:
        raise InsufficientFundsError(
            f"'{sender}' only has {accounts[sender]} gold. Cannot transfer {amount}."
        )
    accounts[sender] -= amount
    accounts[receiver] += amount


def show_balance(name: str) -> int | float:
    """Return the balance of an account."""
    _require_account(name)
    return accounts[name]


def show_all_accounts() -> None:
    """Print every account and its balance."""
    if not accounts:
        print("  (no accounts yet)")
    else:
        for name, balance in accounts.items():
            print(f"  {name}: {balance} gold")


# USER INTERFACE HELPERS


def get_amount_input(prompt: str) -> float:
    """
    Ask the user for a number.
    Raises ValueError (built-in) if they type something that isn't a number.
    """
    raw = input(prompt)
    return float(raw)   # float() raises ValueError on bad input — we let it bubble up


# MENU ACTIONS  (each wraps one task in try/except/else/finally)


def handle_create() -> None:
    name = input("Enter new account name: ").strip().lower()
    try:
        create_account(name)
    except (ValueError, DuplicateAccountError) as e:
        print(f"  Error: {e}")
    else:
        save(accounts)
        print(f"  Account '{name}' created successfully with 0 gold!")
    finally:
        print("  Returning to main menu...\n")


def handle_deposit() -> None:
    name = input("Account name: ").strip().lower()
    try:
        amount = get_amount_input("Amount to deposit: ")
        deposit(name, amount)
    except ValueError:
        print("  Error: Please enter a valid number.")
    except (AccountNotFoundError, InvalidAmountError) as e:
        print(f"  Error: {e}")
    else:
        save(accounts)
        print(f"  Deposited {amount} gold into '{name}'. New balance: {accounts[name]}")
    finally:
        print("  Returning to main menu...\n")


def handle_withdraw() -> None:
    name = input("Account name: ").strip().lower()
    try:
        amount = get_amount_input("Amount to withdraw: ")
        withdraw(name, amount)
    except ValueError:
        print("  Error: Please enter a valid number.")
    except (AccountNotFoundError, InvalidAmountError, InsufficientFundsError) as e:
        print(f"  Error: {e}")
    else:
        save(accounts)
        print(f"  Withdrew {amount} gold from '{name}'. New balance: {accounts[name]}")
    finally:
        print("  Returning to main menu...\n")


def handle_transfer() -> None:
    sender   = input("From account: ").strip().lower()
    receiver = input("To account:   ").strip().lower()
    try:
        amount = get_amount_input("Amount to transfer: ")
        transfer(sender, receiver, amount)
    except ValueError:
        print("  Error: Please enter a valid number.")
    except (AccountNotFoundError, InvalidAmountError,
            InsufficientFundsError, SameAccountTransferError) as e:
        print(f"  Error: {e}")
    else:
        save(accounts)
        print(f"  Transferred {amount} gold from '{sender}' to '{receiver}'.")
    finally:
        print("  Returning to main menu...\n")


def handle_balance() -> None:
    name = input("Account name: ").strip().lower()
    try:
        balance = show_balance(name)
    except AccountNotFoundError as e:
        print(f"  Error: {e}")
    else:
        print(f"  '{name}' has {balance} gold.")
    finally:
        print("  Returning to main menu...\n")


# MAIN MENU LOOP


MENU = """
╔══════════════════════════════╗
║     Magic ATM of Bugdoria    ║
╠══════════════════════════════╣
║  1. Create account           ║
║  2. Deposit gold             ║
║  3. Withdraw gold            ║
║  4. Transfer gold            ║
║  5. Check balance            ║
║  6. Show all accounts        ║
║  7. Exit                     ║
╚══════════════════════════════╝
"""

ACTIONS = {
    "1": handle_create,
    "2": handle_deposit,
    "3": handle_withdraw,
    "4": handle_transfer,
    "5": handle_balance,
    "6": show_all_accounts,
}

def main() -> None:
    print("Welcome to the Magic ATM of Bugdoria!")
    while True:
        print(MENU)
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye, adventurer. May your gold be ever plentiful!")
            break
        elif choice in ACTIONS:
            ACTIONS[choice]()
        else:
            print("  Invalid option. Please choose 1-7.\n")


if __name__ == "__main__":
    main()