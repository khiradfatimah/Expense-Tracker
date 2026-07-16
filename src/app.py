import streamlit as st
import pandas as pd
import db

db.createTable()
st.title("Expense Tracker")

# add expense
st.subheader("💳 Add Expense")
st.write("Tracking your daily expenses.")
with st.form("Add Expense Form", clear_on_submit=True):
    date = st.date_input("Date")
    amount = st.number_input("Amount", min_value=0.01)
    category = st.selectbox(
        "Category", ["Food", "Transport", "Rent", "Cosmetic", "Other"]
    )
    description = st.text_input("Description")

    submitted = st.form_submit_button("Add Expense")

if submitted:
    db.addExpense(str(date), amount, category, description)
    st.success("Expense added!")


# view all expenses
st.subheader("💸 All Expenses")
st.write("See all your expenses.")

expenses = db.getExpenses()
df = pd.DataFrame(expenses, columns=["ID", "Date", "Amount", "Category", "Description"])
st.dataframe(df)

# delete an expense
st.subheader("🚮 Remove Expense")
st.write(
    "Delete an expense that was added by mistake or is something you have returned."
)
expense_ids = [row[0] for row in expenses]
id_to_delete = st.selectbox("Select Expense ID to delete", expense_ids)
selected_expense = db.getExpense(id_to_delete)

if selected_expense:
    st.write(
        f"**Date:** {selected_expense[1]} | "
        f"**Amount:** ${selected_expense[2]:.2f} | "
        f"**Category:** {selected_expense[3]} | "
        f"**Description:** {selected_expense[4]}"
    )
if st.button("Delete Expense", type="primary"):
    db.removeExpense(id_to_delete)
    st.success("Expense Deleted Successfully!")
    st.rerun()


# view selected month's expenses
st.subheader("💷 Monthly Expenses")
st.write("See what you spent in selected month.")

monthly_data = db.getAvailableMonths()
selected_month = st.selectbox("Select Month", monthly_data)
monthly_total = db.getMonthlyTotal(selected_month)
st.metric(label=f"Total for {selected_month}", value=f"${monthly_total:.2f}")


# view all months' expenses
st.subheader("⭕ All Months' Expenses")
st.write("View all your expenses for all months.")
total = db.getAllMonthsTotal()
df_monthly = pd.DataFrame(total, columns=["Month", "Total"]).set_index("Month")
st.bar_chart(df_monthly)
