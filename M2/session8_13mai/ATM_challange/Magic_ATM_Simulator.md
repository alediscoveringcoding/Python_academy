Challenge: Magic ATM Simulator
Story
Welcome to the Magic ATM of Bugdoria.

Your mission is to build a small Python program that simulates a magical ATM system. Users can create accounts, deposit gold, withdraw gold, transfer gold between accounts, and check balances.

There is just one problem:

The users are chaotic.

They will type invalid values, try impossible actions, and break your assumptions whenever they can. Your job is to build a program that handles errors properly using Python exceptions.


Learning Goal
This challenge is designed to help you practice:

try
except
else
finally
raise
built-in exceptions
custom exceptions
clean function design
separating business logic from user interaction


Your Task
Build a menu-driven Python program for a magical ATM.

The program should allow the user to:

create an account
deposit money into an account
withdraw money from an account
transfer money between two accounts
check the balance of an account
exit the program

Use a dictionary to store account balances.

Example idea:

accounts = {
    "alice": 150,
    "bob": 90
}


Technical Requirements
Your solution must include all of the following:

at least 3 functions
at least 2 custom exception classes
at least one try/except/else/finally block
at least one place where you use raise
at least one built-in exception handled properly, such as ValueError
menu-based interaction using input()


Functional Requirements
1. Create Account
Allow the user to create a new account.

Rules:

the account name must not already exist
the account name should not be empty

If something is wrong, raise an appropriate exception.


2. Deposit
Allow the user to deposit money into an existing account.

Rules:

the account must exist
the amount must be a number
the amount must be greater than 0

If something is wrong, raise an appropriate exception.


3. Withdraw
Allow the user to withdraw money from an existing account.

Rules:

the account must exist
the amount must be greater than 0
the account must have enough money

If something is wrong, raise an appropriate exception.


4. Transfer
Allow the user to transfer money from one account to another.

Rules:

both accounts must exist
the sender and receiver must not be the same account
the amount must be greater than 0
the sender must have enough money

If something is wrong, raise an appropriate exception.


5. Check Balance
Allow the user to enter an account name and display its balance.

Rules:

the account must exist

If something is wrong, raise an appropriate exception.


Exception Requirements
You must create your own exceptions for business-rule problems.

You may design your exceptions however you want, but your program should include at least 2 custom exceptions.

Here is one possible direction:

class BankError(Exception):
    pass

class AccountNotFoundError(BankError):
    pass

class InvalidAmountError(BankError):
    pass

class InsufficientFundsError(BankError):
    pass

class DuplicateAccountError(BankError):
    pass

You do not have to use exactly these names, but your exception design should be meaningful and readable.


Important Design Goal
Try to separate your code into two parts:
1. Business Logic
Functions such as:

create_account(...)
deposit(...)
withdraw(...)
transfer(...)
check_balance(...)

These functions should:

validate rules
update data
raise exceptions when something is wrong
2. User Interface
The menu loop should:

ask the user for input
call the right functions
catch exceptions
print friendly error messages

This is an important engineering habit.


Required Use of try, except, else, and finally
Your program must include a real use of all four:

try

around risky code such as input conversion or calling operations that may fail

except

to handle built-in and custom exceptions

else

for code that should run only if no exception happened

finally

for code that should always run, such as a message like "Returning to main menu..."


Suggested Minimum Functions
You may organize your code differently, but a clean version will probably include functions like:

create_account(accounts, name)
deposit(accounts, name, amount)
withdraw(accounts, name, amount)
transfer(accounts, sender, receiver, amount)
show_balance(accounts, name)


Example Behaviors
Your program should handle situations like these gracefully:

user enters "abc" when asked for an amount
user tries to deposit -50
user tries to withdraw more money than they have
user tries to create an account that already exists
user tries to transfer money to the same account
user tries to access an account that does not exist

The program should not crash for these normal mistakes.


Stretch Goals
If you finish early, add one or more of these:
Level 1 Extension
show all accounts and balances
Level 2 Extension
keep a transaction history in a list
Level 3 Extension
add a custom exception for a special rule, such as:
TransferToSameAccountError
EmptyAccountNameError
CursedAccountError
Level 4 Extension
save and load account data from a file
Level 5 Extension
add a fun rule, such as:
Dragon Tax: every withdrawal costs 1 extra coin
Wizard Bonus: deposits over 100 get a bonus
Cursed Account: some account actions randomly fail with a custom exception


Engineering Questions
Before you code, during coding, and after coding, ask yourself these questions.
About the Problem
What are the exact rules of the system?
Which errors come from bad user input?
Which errors come from business rules?
What should happen when the user makes a mistake?
What should happen when everything goes well?
About Exceptions
Which problems should use built-in exceptions like ValueError?
Which problems deserve custom exceptions?
Where should exceptions be raised?
Where should exceptions be caught?
Am I using exceptions to control real error cases, not normal flow unnecessarily?
About Function Design
Should this function print messages, or should it return values / raise exceptions?
Is this function doing too many things at once?
Can I separate validation from user interaction more clearly?
If I change the menu later, will my core functions still work?
About Readability
Are my function names clear?
Are my exception names descriptive?
Would another student understand my code quickly?
Did I choose meaningful variable names?
About Testing Your Thinking
What happens if the account does not exist?
What happens if the amount is zero?
What happens if the amount is negative?
What happens if the user types text instead of a number?
What happens if the sender and receiver are the same?
What happens if the balance is not enough?
About Learning Like an Engineer
Can I explain why I used each exception?
Can I explain why I used else instead of putting everything in try?
Can I explain what finally adds in my program?
If my program fails, do I understand why it failed?
About Using AI Well
Did I ask the AI to explain the concept before asking for code?
Did I ask for hints before asking for the full solution?
Did I compare the AI’s suggestion with my own plan?
Did I test the code instead of trusting it blindly?
Did I ask the AI to explain any line I do not understand?
Could I rebuild this solution on my own after studying it?
About Professional Growth
If this were a real banking system, what extra protections would be needed?
What parts of my code are reusable?
What assumptions am I making?
Where could bugs still appear?
How would I improve this version if I had one more hour?


Deliverables
Submit:

your Python file
a short explanation of your custom exceptions
a short explanation of where you used:
try
except
else
finally


Success Criteria
A strong solution will:

use exceptions clearly and correctly
separate logic from interaction
avoid crashing on normal user mistakes
use custom exceptions in meaningful ways
be clean, readable, and well organized


Final Challenge Prompt
Build the Magic ATM Simulator so that it behaves like a small but robust banking system. Your program must use Python exception handling properly, including custom exceptions, and it must guide the user through errors without crashing.

Make it work.

Make it clean.

Make it resilient.

