import sys
import re
import PyPDF2
import csv
from pathlib import Path
import pandas as pd

DATE = 0
NAME = 1
CHARGE = 2
BALANCE = 3

#regex_pattern = re.compile(r"^\d{2}/\d{2}\s*(Recurring Withdrawal|Withdrawal)")

def parsePdfs(pdfs, regex):
    transactions = list()
    for pdf in pdfs:
        with open(pdf, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                lines = page.extract_text().splitlines()
                for i in range(len(lines)):
                    transaction = regex.search(lines[i])
                    if transaction:
                        transaction_elements = list(transaction.groups())
                        if "Withdrawal POS" in transaction_elements[NAME]:
                            if ((i+1) < len(lines)):
                                transaction_elements[1] = lines[i+1] 
                        transaction_elements.pop(3) # removes the running balance
                        transactions.append(transaction_elements)
    transactions.sort()
    return transactions
        
def extractExpenses(transactions):
    expenses = list()
    expense_regex = re.compile(r"^\d{2}/\d{2}.*-\d*")
    for transaction in transactions:
        if "Transfer" in transaction[NAME]:
            continue
        if float(transaction[CHARGE].replace(",","")) < 0:
            expenses.append(transaction)
    return expenses

def exportToExcel(transactions):
    transactions.insert(0,["Date","Description","Charge"])
    with open('transactions.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(transactions)

    df = pd.read_csv('transactions.csv')
    df.to_excel('transactions.xlsx', index=False)
    

#  main
if len(sys.argv) < 2:
    print("Please provide a directory or file")
    sys.exit(1)

dir = Path(sys.argv[1])
pdfs = dir.glob("*.pdf")

#bank = sys.argv[2] # this will determin the regex pattern that will be used

# stores transactions as a list of lists. Each transaction is split up into [date, description, expense/deposit, balance]
pattern = re.compile(r"^\d{2}/\d{2}/\d{2}|CST.*|-\$\d*.\d*")

with open("new.txt", "w") as f:
    transactions = list()
    transaction = list()
    for pdf in pdfs:
        with open(pdf, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    lines = page.extract_text().splitlines()
                    for i in range(len(lines)):
                        if "Credit for pre-authorized amount" in lines[i]:
                            transaction.clear()
                        temp = pattern.search(lines[i])
                        if temp:
                            f.write(temp.group() + "\n")





def pareseWpcuStatements():
    regex_pattern = re.compile(r"(\d{2}/\d{2})\s+(.*?)\s+(-?[\d,]+\.\d{2})\s+([\d,]+\.\d{2})$")
    transactions = parsePdfs(pdfs, regex_pattern)
    expenses = extractExpenses(transactions)
    exportToExcel(expenses)

    with open("combined_statements.txt", "w") as file:
        for item in transactions:
            for line in item:
                file.write(line + "\t")
            file.write("\n")

def parsePcpStatements():
    regex_pattern = re.compile("")
    transactions = parsePdfs(pdfs, regex_pattern)
    expenses = extractExpenses(transactions)
    exportToExcel(expenses)

    with open("combined_statements.txt", "w") as file:
        for item in transactions:
            for line in item:
                file.write(line + "\t")
            file.write("\n")
