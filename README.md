# 💼 Business Expense Tracker

A modern, interactive expense tracking tool built with **Python**, **Pandas**, and **Streamlit**, designed to help businesses and individuals manage their financial records seamlessly with Excel integration.

🌐 **Live Demo**: [https://business-expense-tracker.streamlit.app](https://business-expense-tracker.streamlit.app)

---

# ✨ Features

- ➕ Add new expense entries with full details
- 🔍 View and filter expenses by date and category
- ✏️ Edit or delete expenses dynamically
- 📊 Monthly and category-wise expense summaries
- 💳 Payment mode-wise analysis
- 📁 Auto-generated Excel sheets
- 📤 Export entire data to CSV format
- 📈 Visual analytics using interactive charts
- 🧾 Optional invoice number and description support

---

# 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nilansh-07/business-expense-tracker.git
   cd business-expense-tracker

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

# ⚙️ Usage

Run the expense tracker:
```bash
python expense_tracker.py
```

## 🧭 Main Menu Options

1. **Add Expense**: Add a new expense entry
   - Date (defaults to today if not specified)
   - Vendor name
   - Category (Travel, Marketing, Office Supplies, etc.)
   - Amount
   - Payment mode (Cash, UPI, Bank Transfer, etc.)
   - Invoice number (optional)

2. **View Expenses**: View all recorded expenses
   - View all expenses
   - Filter by date range
   - Filter by category

3. **Monthly Summary**: View total expenses grouped by month

4. **Category Summary**: View total expenses grouped by category

5. **Export Summary**: Export monthly and category summaries to separate sheets in the Excel file

6. **Exit**: Close the application

# 🧾 Data Storage

All expense data is stored in `expenses.xlsx` in the following format:
- Date
- Vendor
- Category
- Amount
- Payment Mode
- Invoice No

# 📦 Requirements

- Python 3.6 or higher
- pandas
- openpyxl
- tabulate 
