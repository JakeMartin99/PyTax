# PyTax
 A cryptocurrency tax calculator built in Python

Note: Final code was never published here, and prior code has been removed from the public repo as it contained slightly sensitive financial information.

# Utils.py
Provides some convenient utilities for using cmd args to select filenames for IO, reading/writing with financial tx CSVs, and for reformatting tx

# Reformat.py
In the first stage, takes raw exchange CSV and processes it into a new, better formatted CSV:
-Removes redundant/uneccesary tx
-Ensures that both sides of any trade are properly represented
In the second stage, takes reformatted CSV and generates separate tx CSVs for each unique cryptocurrency
In the final stage, uses token-specific CSVs to compute cost basis of each token sale and return total capital gains.
