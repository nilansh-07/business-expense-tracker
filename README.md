# Business Expense Tracker

A command-line interface (CLI) tool for tracking business expenses, storing data in an Excel file.

## Features

- Add new expense entries with details like date, vendor, category, amount, payment mode, and invoice number
- View all expenses with filtering options
- Generate monthly expense summaries
- Generate category-wise expense summaries
- Export summaries to separate Excel sheets

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the expense tracker:
```bash
python expense_tracker.py
```

### Main Menu Options

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

## Data Storage

All expense data is stored in `expenses.xlsx` in the following format:
- Date
- Vendor
- Category
- Amount
- Payment Mode
- Invoice No

## Requirements

- Python 3.6 or higher
- pandas
- openpyxl
- tabulate 