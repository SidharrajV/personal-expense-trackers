import sqlite3
from tabulate import tabulate
from datetime import datetime


conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL
)
''')
conn.commit()


def add_expense():
    try:
        date = input("Enter date (YYYY-MM-DD) [Leave empty for today]: ").strip()
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        category = input("Enter category: ").strip()
        description = input("Enter description (optional): ").strip()
        amount = float(input("Enter amount: "))

        cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                       (date, category, description, amount))
        conn.commit()
        print("✅ Expense added successfully.")
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")

def view_expenses():
    cursor.execute("SELECT id, date, category, description, amount FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID", "Date", "Category", "Description", "Amount"], tablefmt="pretty"))
    else:
        print("No expenses found.")

def delete_expense():
    view_expenses()
    try:
        exp_id = int(input("Enter the ID of the expense to delete: "))
        cursor.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
        conn.commit()
        print("✅ Expense deleted.")
    except ValueError:
        print("❌ Invalid ID.")

def total_spent():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    print(f"💰 Total spent: ${total:.2f}" if total else "No expenses yet.")

def filter_by_category():
    category = input("Enter category to filter by: ").strip()
    cursor.execute("SELECT id, date, category, description, amount FROM expenses WHERE category = ? ORDER BY date DESC", (category,))
    rows = cursor.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID", "Date", "Category", "Description", "Amount"], tablefmt="pretty"))
    else:
        print(f"No expenses found for category '{category}'.")

# --------------------------
# Menu
# --------------------------
def main():
    while True:
        print("\n📒 Personal Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Show Total Spent")
        print("5. Filter by Category")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            total_spent()
        elif choice == '5':
            filter_by_category()
        elif choice == '6':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
