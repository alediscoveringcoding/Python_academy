# exceptions.py

class BankError(Exception):
    """Base class for all Magic ATM errors."""
    pass


class AccountNotFoundError(BankError):
    """Raised when an account name doesn't exist in the system."""
    pass


class DuplicateAccountError(BankError):
    """Raised when someone tries to create an account that already exists."""
    pass


class InvalidAmountError(BankError):
    """Raised when an amount is zero, negative, or not a number."""
    pass


class InsufficientFundsError(BankError):
    """Raised when an account doesn't have enough gold to complete the action."""
    pass


class SameAccountTransferError(BankError):
    """Raised when someone tries to transfer gold to the same account."""
    pass