Cafe Sales Cleanup Challenge
Here’s a 1-hour, beginner-friendly challenge using the Cafe Sales dirty dataset.
Challenge Title
Clean the Cafe Sales Data and Find Suspicious Orders
Your Mission
You have a messy cafe sales dataset.

Your job is to:

clean the data
fix obvious problems
count useful business info
detect suspicious or invalid sales records

Think of it like being the cafe’s data detective.


What You Need to Build
Write a Python program that reads the dataset and answers these questions:

How many rows are in the dataset?
How many rows are valid after cleaning?
How many rows have problems?
What is the total sales amount?
Which product appears most often?
Which rows look suspicious? - what is suspicious?


Data Problems to Look For
Your code should check for issues like:

missing product name
missing price
missing quantity
price stored as text instead of number
quantity stored as text instead of number
extra spaces in text
invalid values like:
negative price
negative quantity
zero quantity
unusually large order total


Suspicious Order Rules
A row should be marked as suspicious if:

price is less than or equal to 0
quantity is less than or equal to 0
order total is greater than a threshold you choose
example: 100 or 200

Simple rule-based detection is perfect here. No fancy AI needed.


Suggested Output
Your program should print something like:

Total rows: 120
Valid rows: 102
Invalid rows: 18
Total sales: 2450.75
Most common product: Coffee
Suspicious rows: 6

You can also print a few suspicious records to inspect them.


Step-by-Step Student Instructions
Part 1: Load the data
import the dataset
store rows in a structure you can loop through
print the first few rows so you understand the data
Part 2: Clean the values
For each row:

remove extra spaces from text
convert price to float
convert quantity to int
handle missing or broken values carefully
Part 3: Validate each row
Check whether the row is:

valid
invalid
suspicious

You can keep separate counters or lists for these.
Part 4: Analyze the cleaned data
Calculate:

total valid sales
most common product
number of invalid rows
number of suspicious rows
Part 5: Print a clean summary
Make your output easy to read.


Beginner Hints
Use strip() for extra spaces
Use float() and int() for conversion
Use try/except if conversion fails
Use a dictionary to count products
Use if statements for anomaly rules


Nice Simple Structure
You can break your program into small parts:

clean_value(...)
is_valid_row(...)
is_suspicious_row(...)
main loop
summary print section

That structure keeps things clean and easier to debug.


1-Hour Version
If you want to finish in one hour, focus only on these:

clean product, price, quantity
reject missing or invalid rows
compute total sales
find most common product
flag suspicious rows

Skip anything extra unless you finish early.


Bonus If You Finish Early
show top 3 products
calculate average order total
save suspicious rows into a new file
print the row number of each bad record


Success Goal
By the end, you should be able to practice:

strings
numbers
lists
dictionaries
loops
conditionals
basic error handling
simple anomaly detection


Mini Challenge Prompt for Students
You are given a messy cafe sales dataset.
Clean the data, remove invalid records, calculate total sales,
find the most common product, and detect suspicious orders.
Recommended Next Step
If you want, I can now give you one of these:

A. A very short starter template
B. A step-by-step solution outline without full code
C. A teacher-ready challenge sheet with inputs, tasks, and expected outputs
Status
The challenge is now defined and scoped to fit about one hour.
Data Set
https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training

