import json

transactions = []


def new_transaction():

    while True:
        transaction = {}

        date = input("Enter date: ")
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        transaction_type = input("Enter type(expense/income): ")
        transaction["date"] = date
        transaction["amount"] = amount
        transaction["category"] = category
        transaction["type"] = transaction_type



        transactions.append(transaction)
        with open("transactions.json", "w") as file:
            json.dump(transactions, file)



        another = input("Would you like to enter another transaction (y/n): ")
        if another == "y":
            continue
        elif another == "n":
            break

def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            transactions = json.load(file)
        return transactions
    except FileNotFoundError:
        return []



def total_income():
    total = 0
    for transaction in transactions:
        if transaction["type"] == "income":
            total += transaction["amount"]
    return total



def total_expense():
    total = 0
    for transaction in transactions:
        if transaction["type"] == "expense":
            total += transaction["amount"]
    return total

def balance():
    balance = total_income() - total_expense()
    return balance

def show_summary():
    print("Total income:", total_income())
    print("Total expense:", total_expense())
    print("Balance:", balance())

def show_transactions():
    for transaction in transactions:
        print(transaction["date"], transaction["amount"], transaction["category"], transaction["type"])


def menu():
    global transactions


    transactions = load_transactions()

    while True:
        print("1 - Add new transaction")
        print("2 - Show summary")
        print("3 - Show transactions")
        print("4 - Exit")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                new_transaction()
            elif choice == 2:
                show_summary()
            elif choice == 3:
                show_transactions()
            elif choice == 4:
                break
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter a valid number")

menu()