import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt


# ---------- FILE INIT ----------
FILE = "expenses.csv"
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        csv.writer(f).writerow(["Date", "Category", "Amount", "Note"])

# ---------- FUNCTIONS ----------
def add_expense():
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()
    note = note_entry.get().strip()

    if not category or not amount:
        messagebox.showerror("Error", "Category and Amount are required")
        return

    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE, "a", newline="") as f:
        csv.writer(f).writerow([date, category, amount, note])

    messagebox.showinfo("Success", "Expense Added")

    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)


def view_expenses():
    output.delete(*output.get_children())
    total = 0

    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for date, category, amount, note in reader:
            output.insert("", "end", values=(date, category, amount, note))
            total += float(amount)

    total_label.config(text=f"Total Spending: ₹{total}")


def category_summary():
    categories = {}

    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for _, category, amount, _ in reader:
            categories[category] = categories.get(category, 0) + float(amount)

    if not categories:
        messagebox.showinfo("Info", "No data available")
        return

    plt.figure(figsize=(6, 6))
    plt.pie(categories.values(),labels=categories.keys(),autopct="%1.1f%%",startangle=90)
    plt.title("Spending by Category")
    plt.show()


def insights():
    expenses = []

    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for _, category, amount, note in reader:
            expenses.append((float(amount), category, note))

    if not expenses:
        messagebox.showinfo("Info", "No data available")
        return

    high = max(expenses)
    low = min(expenses)

    messagebox.showinfo("Insights",f"Highest: ₹{high[0]} ({high[1]} - {high[2]})\n"f"Lowest: ₹{low[0]} ({low[1]} - {low[2]})")

# ---------- GUI ----------
root = tk.Tk()
root.title("Student Expense Tracker")
root.geometry("1536x864")
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use("clam")

# ---------- HEADER ----------
header = tk.Frame(root, bg="#1e293b", height=60)
header.pack(fill="x")

tk.Label(header,text="Student Expense Tracker",bg="#1e293b",fg="white",font=("Segoe UI", 18, "bold")).pack(pady=12)

# ---------- MAIN CONTENT ----------
content = tk.Frame(root, bg="#C9C8A1")
content.pack(fill="both", expand=True, padx=20, pady=20)

# ---------- LEFT PANEL ----------
left = tk.Frame(content, bg="white", bd=1, relief="solid")
left.pack(side="left", fill="y", padx=(0, 15))

tk.Label(left,text="Add Expense",bg="white",font=("Segoe UI", 14, "bold")).pack(pady=10)

form = tk.Frame(left, bg="white")
form.pack(padx=15)

ttk.Label(form, text="Category").grid(row=0, column=0, sticky="w", pady=5)
ttk.Label(form, text="Amount").grid(row=1, column=0, sticky="w", pady=5)
ttk.Label(form, text="Note").grid(row=2, column=0, sticky="w", pady=5)

category_entry = ttk.Entry(form, width=25)
amount_entry = ttk.Entry(form, width=25)
note_entry = ttk.Entry(form, width=25)

category_entry.grid(row=0, column=1, pady=5)
amount_entry.grid(row=1, column=1, pady=5)
note_entry.grid(row=2, column=1, pady=5)

ttk.Button(left,text="Add Expense",command=add_expense).pack(pady=15)

# ---------- RIGHT PANEL ----------
right = tk.Frame(content, bg="white", bd=1, relief="solid")
right.pack(side="right", fill="both", expand=True)

controls = tk.Frame(right, bg="white")
controls.pack(pady=10)

ttk.Button(controls, text="View Expenses", command=view_expenses).grid(row=0, column=0, padx=5)
ttk.Button(controls, text="Category Summary", command=category_summary).grid(row=0, column=1, padx=5)
ttk.Button(controls, text="Insights", command=insights).grid(row=0, column=2, padx=5)

columns = ("Date", "Category", "Amount", "Note")
output = ttk.Treeview(right, columns=columns, show="headings", height=15)

for col in columns:
    output.heading(col, text=col)
    output.column(col, anchor="center")

output.pack(fill="both", expand=True, padx=10, pady=10)

total_label = ttk.Label(right, text="Total Spending: ₹0", font=("Segoe UI", 11, "bold"))
total_label.pack(pady=5)

root.mainloop()
