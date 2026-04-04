import sys
import re
import PyPDF2
from pathlib import Path

DATE = 0
NAME = 1
CHARGE = 2
BALANCE = 3

#regex_pattern = re.compile(r"^\d{2}/\d{2}\s*(Recurring Withdrawal|Withdrawal)")
regex_pattern = re.compile(r"(\d{2}/\d{2})\s+(.*?)\s+(-?[\d,]+\.\d{2})\s+([\d,]+\.\d{2})$")

def parsePdfs(pdfs):
    transactions = list()
    for pdf in pdfs:
        with open(pdf, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                lines = page.extract_text().splitlines()
                for i in range(len(lines)):
                    transaction = regex_pattern.search(lines[i])
                    if transaction:
                        transaction_elements = list(transaction.groups())
                        if "Withdrawal POS" in transaction_elements[NAME]:
                            if ((i+1) < len(lines)):
                                transaction_elements[1] = lines[i+1] 
                        transactions.append(transaction_elements)
    transactions.sort()
    return transactions
        
def extractExpenses(transactions):
    expense_regex = re.compile(r"^\d{2}/\d{2}.*-\d*")
    for item in transactions:
        if "Withdrawal Transfer To Share 91" in item:
            continue
        if expense_regex.search(item):
            print(item)


#  main
if len(sys.argv) < 2:
    print("Please provide a directory or file")
    sys.exit(1)

dir = Path(sys.argv[1])
pdfs = dir.glob("*.pdf")

# stores transactions as a list of lists. Each transaction is split up into [date, description, expense/deposit, balance]
transactions = parsePdfs(pdfs)

#extractExpenses(transactions)
with open("combined_statements.txt", "w") as file:
    for item in transactions:
        for line in item:
            file.write(line + "\t")
        file.write("\n")


