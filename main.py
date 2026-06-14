import json
from datetime import datetime

FILENAME = "transactions.json"
transactions = []

def save_data():
    with open(FILENAME, "w") as f:
        json.dump(transactions, f, indent=4)



def load_data():
    global transactions
    try:
        with open(FILENAME, "r") as f:
            transactions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        transactions = []


def get_amount():
    while True:
        try:
            amount = float(input("Enter Amount: "))
            if amount <=0:
                print("Amount must be greater than zero.")
            else:
                return amount
        except ValueError:
            print("Invalid amount. Enter a number!")

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def add_income():
    while True:
        source = input("Enter Source: ")
        if not source:
            print(" Source cannot be empty!")
            continue
        amount = get_amount()
        transactions.append({
             "type": "income", 
             "source": source,
             "amount": amount,
             "date": current_time()
        })
        save_data()
        print("Income added!")

        choice = input("Add another income? (y/n): ").lower()
        if choice != "y":
            return


def add_expense():
    while True:
        category = input("Enter Category: ")
        if not category:
            print("Category cannot be empty!")
            continue
        amount = get_amount()
        transactions.append({
            "type": "expense",
            "category": category,
            "amount": amount
         })
        save_data()
        print("Expense added!")
        choice = input("Add another Expense? (y/n): ").lower()
        if choice != "y":
            return


def view_transactions():
    if not transactions:
        print("No transactions yet.")
        return
    

    print("\n--- TRANSACTIONS ---")
    for i,t in enumerate(transactions):
        date = t.get("date", "N/A")
        label = t.get("source") or t.get("category")
        kind = "Income " if t["type"] == "income" else "Expense"
        print(f"[{i+1}] {kind} | {label} | Rs.{t['amount']:.2f} | {date}")

def delete_transactions():
    if not transactions:
        print("No transactions to delete.")
        return 
    
    view_transactions()
    index = int(input("\n Enter transaction number to delete(0 to cancel): "))
    if index == 0:
        return
    removed = transactions.pop(index - 1)
    save_data()
    label = removed.get("source") or removed.get("category")
    print(f"Deleted: {label} | Rs.{removed['amount']:.2f}")


def check_balance():
    total_income = 0
    total_expense = 0
    for t in transactions:
        if t["type"] == "income":
            total_income += t["amount"]
        else:
            total_expense += t["amount"]

    print("\n--- BALANCE ---")
    print(f"Income  : {total_income: .2f}")
    print(f"Expense : {total_expense: .2f}")
    print(f"Balance : {total_income - total_expense: .2f}")


def monthly_summary():
    if not transactions:
        print("No transactions yet.")
        return
    summary = {}

    for t in transactions:
        date = t.get("date", "Unknown")
        month = date[:7]
        summary.setdefault(month, [0, 0])
        if t["type"] == "income":
            summary[month][0] += t["amount"]
        else:
            summary[month][1] += t["amount"]


    print("\n---Monthly Summary---")
    for month, (inc, exp) in sorted(summary.items()):
        print(f"\n{month} | Rs.{inc:.2f} in | Rs.{exp:.2f} out | Net: Rs.{inc - exp:.2f}")

answer = input("Load previous transactions? (yes/no): ")
if answer == "yes":
    load_data()
    print(f"Loaded {len(transactions)} transaction(s).")
else:
    transactions = []

while True:

    print("\n===== PERSONAL FINANCE MANAGER =====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. Check Balance")
    print("5. Monthly Summary")
    print("6. Delete Transaction")
    print("7. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_income()
    elif choice == "2":
        add_expense()
    elif choice == "3":
        view_transactions()
    elif choice == "4":
        check_balance()
    elif choice == "5":
        monthly_summary()
    elif choice == "6":
        delete_transactions()
    elif choice == "7":
        print("Ended!")    

        break
    else:
        print("Invalid choice.")
       