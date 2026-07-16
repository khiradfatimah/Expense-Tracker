import sqlite3
from datetime import datetime


def createTable():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL, 
            category TEXT,
            description TEXT
            )
        """)
    connection.commit()
    connection.close()


# function for adding expense
def addExpense(date, amount, category, description):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        connection.close()
        return

    try:
        amount = float(amount)
        if amount <= 0:
            print("Amount must be a positive number!")
            connection.close()
            return
    except ValueError:
        print("Amount must be a number!")
        connection.close()
        return

    cursor.execute(
        "INSERT INTO expenses(date, amount, category, description) VALUES (?,?,?,?)",
        (date, amount, category, description),
    )
    connection.commit()
    connection.close()


# function for removing/deleting expense
def removeExpense(expense_id):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM expenses where id = ?", (expense_id,))
    connection.commit()
    connection.close()


# function for getting expense
def getExpense(expense_id):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    result = cursor.fetchone()
    connection.close()
    return result


# function for getting expenses
def getExpenses():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM expenses",
    )
    result = cursor.fetchall()
    connection.close()
    return result


# function for getting monthly total
def getMonthlyTotal(year_month):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', date)=?",
        (year_month,),
    )
    result = cursor.fetchone()
    connection.close()
    return result[0] if result[0] is not None else 0


# function to get list of available months
def getAvailableMonths():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT DISTINCT strftime('%Y-%m', date) as month
        FROM expenses
        ORDER BY month DESC""")
    result = cursor.fetchall()
    connection.close()
    return [row[0] for row in result]


# function for getting all available months' total
def getAllMonthsTotal():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total
        FROM expenses
        GROUP BY month
        ORDER BY month""")
    result = cursor.fetchall()
    connection.close()
    return result


if __name__ == "__main__":
    createTable()
