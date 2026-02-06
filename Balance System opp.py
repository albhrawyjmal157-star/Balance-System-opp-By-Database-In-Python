# =========================================== Three Day =========================================
import os
import time
import sqlite3

def Clear_Screen():
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')


# ================================= Set Up =====================================================
db = sqlite3.connect("Balance System.db")
cr = db.cursor()

cr.execute(
    "CREATE TABLE IF NOT EXISTS accounts (name TEXT, id INTEGER, balance REAL)"
)
db.commit()


class Bank:
    def __init__(self, name, id, balance):
        self.name = name
        self.id = id
        self.__balance = balance

    def Show(self):
        print(f"Name    : {self.name}")
        print(f"ID      : {self.id}")
        print(f"Balance : {self.__balance}")

    def ReturnBalance(self):
        return self.__balance

    def Deposit(self, value):
        self.__balance += value

    def Withdraw(self, value):
        self.__balance -= value


while True:
    print("1 - Create Account")
    print("2 - Show Balance")
    print("3 - Deposit")
    print("4 - Withdraw")
    print("5 - Exit")

    try:
        choice = int(input("Enter Your Choice: ").strip())
    except ValueError:
        print("Only numbers are allowed.")
        Clear_Screen()
        continue

    # ---------------- Create Account ----------------
    if choice == 1:
        name = input("Enter Name: ").strip().lower().capitalize()
        try:
            id = int(input("Enter ID: "))
        except ValueError:
            print("Only numbers are allowed.")
            Clear_Screen()
            continue

        cr.execute("SELECT id FROM accounts WHERE id = ?", (id,))
        result = cr.fetchone()
        if result:
            print("Account already exists.")
            Clear_Screen()
            continue

        balance = float(input("Enter Balance: "))
        user = Bank(name, id, balance)
        cr.execute(
            "INSERT INTO accounts (name, id, balance) VALUES (?, ?, ?)",
            (user.name, user.id, user.ReturnBalance())
        )
        print("Account created successfully.")

    # ---------------- Show Balance ----------------
    elif choice == 2:
        try:
            id = int(input("Enter ID: "))
        except ValueError:
            print("Only numbers are allowed.")
            Clear_Screen()
            continue

        cr.execute("SELECT * FROM accounts WHERE id = ?", (id,))
        result = cr.fetchone()
        if result:
            user = Bank(result[0], result[1], result[2])
            print(f"Balance: {user.ReturnBalance()}")
        else:
            print("Account not found.")

    # ---------------- Deposit ----------------
    elif choice == 3:
        name = input("Enter Name: ").strip().lower().capitalize()
        id = int(input("Enter ID: "))

        cr.execute(
            "SELECT * FROM accounts WHERE name = ? AND id = ?",
            (name, id)
        )
        result = cr.fetchone()
        if not result:
            print("Account not found.")
            Clear_Screen()
            continue

        user = Bank(result[0], result[1], result[2])
        value = int(input("Enter deposit amount: "))

        if value < 0:
            print("Invalid value.")
            Clear_Screen()
            continue

        user.Deposit(value)
        cr.execute(
            "UPDATE accounts SET balance = ? WHERE id = ?",
            (user.ReturnBalance(), user.id)
        )
        print("Deposit completed successfully.")

    # ---------------- Withdraw ----------------
    elif choice == 4:
        name = input("Enter Name: ").strip().lower().capitalize()
        id = int(input("Enter ID: "))

        cr.execute(
            "SELECT * FROM accounts WHERE name = ? AND id = ?",
            (name, id)
        )
        result = cr.fetchone()
        if not result:
            print("Account not found.")
            Clear_Screen()
            continue

        user = Bank(result[0], result[1], result[2])
        value = int(input("Enter withdrawal amount: "))

        if value < 0:
            print("Invalid value.")
            Clear_Screen()
            continue

        if value > user.ReturnBalance():
            print("Insufficient balance.")
            Clear_Screen()
            continue

        user.Withdraw(value)
        cr.execute(
            "UPDATE accounts SET balance = ? WHERE id = ?",
            (user.ReturnBalance(), user.id)
        )
        print("Withdrawal completed successfully.")

    elif choice == 5:
        print("Goodbye 👋")
        break

    db.commit()
    Clear_Screen()
