import tkinter as tk
from tkinter import ttk, messagebox
import json


# =========================
# COLORS
# =========================

BG = "#F4F1EA"
NAVY = "#1F2A44"
WHITE = "#FFFFFF"
LIGHT_NAVY = "#344563"
GREEN = "#4F7C62"
RED = "#B85C5C"
GREY = "#777777"


# =========================
# DATA
# =========================

def save_transactions():
    with open("transactions.json", "w") as file:
        json.dump(transactions, file, indent=4)


def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


transactions = load_transactions()


# =========================
# CALCULATIONS
# =========================

def total_income():
    total = 0

    for transaction in transactions:
        if transaction["type"] == "Income":
            total += transaction["amount"]

    return total


def total_expense():
    total = 0

    for transaction in transactions:
        if transaction["type"] == "Expense":
            total += transaction["amount"]

    return total


def balance():
    return total_income() - total_expense()


# =========================
# ADD TRANSACTION
# =========================

def new_transaction():

    transaction_window = tk.Toplevel(window)
    transaction_window.title("Add Transaction")
    transaction_window.geometry("500x500")
    transaction_window.configure(bg=BG)
    transaction_window.resizable(False, False)

    title = tk.Label(
        transaction_window,
        text="Add Transaction",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=NAVY
    )
    title.pack(pady=(30, 25))

    # DATE

    tk.Label(
        transaction_window,
        text="Date",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(anchor="w", padx=60)

    date_entry = tk.Entry(
        transaction_window,
        font=("Arial", 12),
        width=35
    )
    date_entry.pack(pady=(5, 15))

    # AMOUNT

    tk.Label(
        transaction_window,
        text="Amount",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(anchor="w", padx=60)

    amount_entry = tk.Entry(
        transaction_window,
        font=("Arial", 12),
        width=35
    )
    amount_entry.pack(pady=(5, 15))

    # CATEGORY

    tk.Label(
        transaction_window,
        text="Category",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(anchor="w", padx=60)

    category_box = ttk.Combobox(
        transaction_window,
        values=[
            "Salary",
            "Food",
            "Transport",
            "Bills",
            "Shopping",
            "Entertainment",
            "Health",
            "Other"
        ],
        state="readonly",
        width=33
    )
    category_box.pack(pady=(5, 15))

    # TYPE

    tk.Label(
        transaction_window,
        text="Type",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(anchor="w", padx=60)

    type_box = ttk.Combobox(
        transaction_window,
        values=["Income", "Expense"],
        state="readonly",
        width=33
    )
    type_box.pack(pady=(5, 25))

    # SAVE TRANSACTION

    def save_transaction():

        date = date_entry.get()
        amount_value = amount_entry.get()
        category = category_box.get()
        transaction_type = type_box.get()

        if not date or not amount_value or not category or not transaction_type:
            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )
            return

        try:
            amount = float(amount_value)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be a number."
            )
            return

        if amount <= 0:
            messagebox.showerror(
                "Error",
                "Amount must be greater than 0."
            )
            return

        transaction = {
            "date": date,
            "amount": amount,
            "category": category,
            "type": transaction_type
        }

        transactions.append(transaction)

        save_transactions()

        update_summary()

        messagebox.showinfo(
            "Success",
            "Transaction added successfully."
        )

        transaction_window.destroy()

    save_button = tk.Button(
        transaction_window,
        text="Save Transaction",
        command=save_transaction,
        bg=NAVY,
        fg=WHITE,
        activebackground=LIGHT_NAVY,
        activeforeground=WHITE,
        font=("Arial", 12, "bold"),
        relief="flat",
        cursor="hand2",
        width=22,
        pady=8
    )
    save_button.pack()


# =========================
# SHOW TRANSACTIONS
# =========================

def show_transactions():

    transaction_window = tk.Toplevel(window)
    transaction_window.title("Transactions")
    transaction_window.geometry("700x500")
    transaction_window.configure(bg=BG)

    title = tk.Label(
        transaction_window,
        text="Transactions",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=NAVY
    )
    title.pack(pady=20)

    columns = ("Date", "Amount", "Category", "Type")

    tree = ttk.Treeview(
        transaction_window,
        columns=columns,
        show="headings",
        height=15
    )

    tree.heading("Date", text="Date")
    tree.heading("Amount", text="Amount")
    tree.heading("Category", text="Category")
    tree.heading("Type", text="Type")

    tree.column("Date", width=130)
    tree.column("Amount", width=120)
    tree.column("Category", width=180)
    tree.column("Type", width=120)

    tree.pack(
        padx=20,
        pady=10,
        fill="both",
        expand=True
    )

    for transaction in transactions:

        tree.insert(
            "",
            "end",
            values=(
                transaction["date"],
                f"{transaction['amount']:.2f}",
                transaction["category"],
                transaction["type"]
            )
        )


# =========================
# SUMMARY WINDOW
# =========================

def summary():

    summary_window = tk.Toplevel(window)
    summary_window.title("Summary")
    summary_window.geometry("450x400")
    summary_window.configure(bg=BG)
    summary_window.resizable(False, False)

    title = tk.Label(
        summary_window,
        text="Financial Summary",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=NAVY
    )
    title.pack(pady=(30, 35))

    income = tk.Label(
        summary_window,
        text=f"Income\n{total_income():.2f} PLN",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=GREEN,
        width=25,
        pady=15
    )
    income.pack(pady=8)

    expenses = tk.Label(
        summary_window,
        text=f"Expenses\n{total_expense():.2f} PLN",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=RED,
        width=25,
        pady=15
    )
    expenses.pack(pady=8)

    current_balance = balance()

    balance_color = GREEN if current_balance >= 0 else RED

    balance_label = tk.Label(
        summary_window,
        text=f"Balance\n{current_balance:.2f} PLN",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=balance_color,
        width=25,
        pady=15
    )
    balance_label.pack(pady=8)


# =========================
# UPDATE MAIN SUMMARY
# =========================

def update_summary():

    income_value.config(
        text=f"{total_income():.2f} PLN"
    )

    expense_value.config(
        text=f"{total_expense():.2f} PLN"
    )

    current_balance = balance()

    balance_value.config(
        text=f"{current_balance:.2f} PLN"
    )

    if current_balance >= 0:
        balance_value.config(fg=GREEN)
    else:
        balance_value.config(fg=RED)


# =========================
# MAIN WINDOW
# =========================

window = tk.Tk()

window.title("Personal Finance")
window.geometry("650x650")
window.configure(bg=BG)
window.resizable(False, False)


# HEADER

header = tk.Frame(
    window,
    bg=NAVY,
    height=130
)
header.pack(fill="x")

title = tk.Label(
    header,
    text="Personal Finance",
    font=("Arial", 25, "bold"),
    bg=NAVY,
    fg=WHITE
)
title.pack(pady=(25, 5))

subtitle = tk.Label(
    header,
    text="Manage your money with ease",
    font=("Arial", 11),
    bg=NAVY,
    fg=WHITE
)
subtitle.pack()


# =========================
# SUMMARY CARDS
# =========================

cards_frame = tk.Frame(
    window,
    bg=BG
)
cards_frame.pack(pady=35)


# INCOME

income_card = tk.Frame(
    cards_frame,
    bg=WHITE,
    width=175,
    height=110
)
income_card.pack(side="left", padx=8)
income_card.pack_propagate(False)

tk.Label(
    income_card,
    text="Income",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    fg=GREY
).pack(pady=(15, 5))

income_value = tk.Label(
    income_card,
    text=f"{total_income():.2f} PLN",
    font=("Arial", 17, "bold"),
    bg=WHITE,
    fg=GREEN
)
income_value.pack()


# EXPENSES

expense_card = tk.Frame(
    cards_frame,
    bg=WHITE,
    width=175,
    height=110
)
expense_card.pack(side="left", padx=8)
expense_card.pack_propagate(False)

tk.Label(
    expense_card,
    text="Expenses",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    fg=GREY
).pack(pady=(15, 5))

expense_value = tk.Label(
    expense_card,
    text=f"{total_expense():.2f} PLN",
    font=("Arial", 17, "bold"),
    bg=WHITE,
    fg=RED
)
expense_value.pack()


# BALANCE

balance_card = tk.Frame(
    cards_frame,
    bg=WHITE,
    width=175,
    height=110
)
balance_card.pack(side="left", padx=8)
balance_card.pack_propagate(False)

tk.Label(
    balance_card,
    text="Balance",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    fg=GREY
).pack(pady=(15, 5))

balance_value = tk.Label(
    balance_card,
    text=f"{balance():.2f} PLN",
    font=("Arial", 17, "bold"),
    bg=WHITE,
    fg=GREEN if balance() >= 0 else RED
)
balance_value.pack()


# =========================
# BUTTONS
# =========================

buttons_frame = tk.Frame(
    window,
    bg=BG
)
buttons_frame.pack(pady=20)


# ADD TRANSACTION

add_button = tk.Button(
    buttons_frame,
    text="Add Transaction",
    command=new_transaction,
    bg=NAVY,
    fg=WHITE,
    activebackground=LIGHT_NAVY,
    activeforeground=WHITE,
    font=("Arial", 12, "bold"),
    relief="flat",
    cursor="hand2",
    width=22,
    pady=10
)
add_button.pack(pady=7)


# SUMMARY

summary_button = tk.Button(
    buttons_frame,
    text="Summary",
    command=summary,
    bg=NAVY,
    fg=WHITE,
    activebackground=LIGHT_NAVY,
    activeforeground=WHITE,
    font=("Arial", 12, "bold"),
    relief="flat",
    cursor="hand2",
    width=22,
    pady=10
)
summary_button.pack(pady=7)


# TRANSACTIONS

transactions_button = tk.Button(
    buttons_frame,
    text="Transactions",
    command=show_transactions,
    bg=NAVY,
    fg=WHITE,
    activebackground=LIGHT_NAVY,
    activeforeground=WHITE,
    font=("Arial", 12, "bold"),
    relief="flat",
    cursor="hand2",
    width=22,
    pady=10
)
transactions_button.pack(pady=7)


# EXIT

exit_button = tk.Button(
    buttons_frame,
    text="Exit",
    command=window.destroy,
    bg=NAVY,
    fg=WHITE,
    activebackground=LIGHT_NAVY,
    activeforeground=WHITE,
    font=("Arial", 12, "bold"),
    relief="flat",
    cursor="hand2",
    width=22,
    pady=10
)
exit_button.pack(pady=7)


# =========================
# RUN
# =========================

window.mainloop()