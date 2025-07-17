import streamlit as st
import pandas as pd
from datetime import datetime
import os
import tempfile
from pathlib import Path

class ExpenseTracker:
    def __init__(self, excel_file="expenses.xlsx"):
        self.excel_file = excel_file
        self.initialize_excel()

    def initialize_excel(self):
        """Initialize Excel file with required columns if it doesn't exist"""
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=[
                'Date', 'Vendor', 'Category', 'Amount', 
                'Payment Mode', 'Invoice No', 'Description'
            ])
            df.to_excel(self.excel_file, index=False)

    def save_to_excel(self, df):
        """Save DataFrame to Excel and update all sheets"""
        with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
            # Save main expenses sheet
            df.to_excel(writer, sheet_name='Expenses', index=False)
            
            # Create and save monthly summary
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
                monthly_summary = df.groupby(df['Date'].dt.strftime('%Y-%m'))['Amount'].sum()
                monthly_summary.to_excel(writer, sheet_name='Monthly Summary')
                
                # Create and save category summary
                category_summary = df.groupby('Category')['Amount'].sum()
                category_summary.to_excel(writer, sheet_name='Category Summary')
                
                # Create and save payment mode summary
                payment_summary = df.groupby('Payment Mode')['Amount'].sum()
                payment_summary.to_excel(writer, sheet_name='Payment Summary')

    def add_expense(self, date, vendor, category, amount, payment_mode, invoice_no, description):
        """Add a new expense entry"""
        # Create new entry
        new_entry = {
            'Date': date,
            'Vendor': vendor,
            'Category': category,
            'Amount': amount,
            'Payment Mode': payment_mode,
            'Invoice No': invoice_no,
            'Description': description
        }

        # Read existing data
        df = pd.read_excel(self.excel_file)
        
        # Append new entry
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        
        # Save to Excel with all sheets updated
        self.save_to_excel(df)
        st.success("Expense added successfully!")

    def update_expense(self, index, date, vendor, category, amount, payment_mode, invoice_no, description):
        """Update an existing expense entry"""
        df = pd.read_excel(self.excel_file)
        
        if 0 <= index < len(df):
            df.loc[index] = {
                'Date': date,
                'Vendor': vendor,
                'Category': category,
                'Amount': amount,
                'Payment Mode': payment_mode,
                'Invoice No': invoice_no,
                'Description': description
            }
            
            self.save_to_excel(df)
            st.success("Expense updated successfully!")
        else:
            st.error("Invalid expense index!")

    def delete_expense(self, index):
        """Delete an expense entry"""
        df = pd.read_excel(self.excel_file)
        
        if 0 <= index < len(df):
            df = df.drop(index)
            self.save_to_excel(df)
            st.success("Expense deleted successfully!")
        else:
            st.error("Invalid expense index!")

    def get_expenses(self):
        """Get all expenses"""
        return pd.read_excel(self.excel_file)

    def get_monthly_summary(self):
        """Get monthly expense summary"""
        df = self.get_expenses()
        if df.empty:
            return pd.DataFrame()
        
        df['Date'] = pd.to_datetime(df['Date'])
        return df.groupby(df['Date'].dt.strftime('%Y-%m'))['Amount'].sum()

    def get_category_summary(self):
        """Get category-wise expense summary"""
        df = self.get_expenses()
        if df.empty:
            return pd.DataFrame()
        
        return df.groupby('Category')['Amount'].sum()

    def get_payment_summary(self):
        """Get payment mode-wise expense summary"""
        df = self.get_expenses()
        if df.empty:
            return pd.DataFrame()
        
        return df.groupby('Payment Mode')['Amount'].sum()

    def export_to_csv(self):
        """Export expenses to CSV"""
        df = self.get_expenses()
        if not df.empty:
            csv = df.to_csv(index=False)
            return csv
        return None

def get_excel_files():
    """Get all Excel files in the current directory"""
    return [f for f in os.listdir() if f.endswith('.xlsx')]

def create_new_excel_file(filename):
    """Create a new Excel file with required columns"""
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'
    
    df = pd.DataFrame(columns=[
        'Date', 'Vendor', 'Category', 'Amount', 
        'Payment Mode', 'Invoice No', 'Description'
    ])
    df.to_excel(filename, index=False)
    return filename

def main():
    st.set_page_config(
        page_title="Business Expense Tracker",
        page_icon="💰",
        layout="wide"
    )

    st.title("💰 Business Expense Tracker")
    
    # File selection
    st.sidebar.title("File Management")
    
    # Get existing Excel files
    excel_files = get_excel_files()
    
    # File selection options
    file_option = st.sidebar.radio(
        "Select or Create File",
        ["Select Existing File", "Create New File"]
    )
    
    if file_option == "Select Existing File":
        if not excel_files:
            st.sidebar.warning("No Excel files found in the current directory!")
            return
        
        selected_file = st.sidebar.selectbox(
            "Select Excel File",
            excel_files
        )
        tracker = ExpenseTracker(selected_file)
    
    else:  # Create New File
        new_filename = st.sidebar.text_input(
            "Enter new file name (without extension)",
            value="expenses"
        )
        if st.sidebar.button("Create File"):
            if new_filename:
                try:
                    selected_file = create_new_excel_file(new_filename)
                    tracker = ExpenseTracker(selected_file)
                    st.sidebar.success(f"Created new file: {selected_file}")
                except Exception as e:
                    st.sidebar.error(f"Error creating file: {str(e)}")
            else:
                st.sidebar.error("Please enter a file name!")
            return
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Add Expense", "View/Edit Expenses", "Monthly Summary", "Category Summary", "Payment Summary", "Export Data"]
    )

    if page == "Add Expense":
        st.header("Add New Expense")
        
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date", value=datetime.now())
            vendor = st.text_input("Vendor Name")
            category = st.selectbox(
                "Category",
                ["Travel", "Marketing", "Office Supplies", "Utilities", "Meals", "Other"]
            )
            description = st.text_area("Description (Optional)")
        
        with col2:
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            payment_mode = st.selectbox(
                "Payment Mode",
                ["Cash", "UPI", "Bank Transfer", "Credit Card", "Other"]
            )
            invoice_no = st.text_input("Invoice Number (Optional)")

        if st.button("Add Expense"):
            tracker.add_expense(
                date=date.strftime("%Y-%m-%d"),
                vendor=vendor,
                category=category,
                amount=amount,
                payment_mode=payment_mode,
                invoice_no=invoice_no,
                description=description
            )

    elif page == "View/Edit Expenses":
        st.header("View/Edit Expenses")
        
        df = tracker.get_expenses()
        
        if df.empty:
            st.info("No expenses recorded yet!")
        else:
            # Add filters
            col1, col2 = st.columns(2)
            
            with col1:
                date_range = st.date_input(
                    "Filter by Date Range",
                    value=(df['Date'].min(), df['Date'].max()),
                    min_value=df['Date'].min(),
                    max_value=df['Date'].max()
                )
            
            with col2:
                category_filter = st.selectbox(
                    "Filter by Category",
                    ["All"] + list(df['Category'].unique())
                )
            
            # Apply filters
            if len(date_range) == 2:
                mask = (df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))
                df = df[mask]
            
            if category_filter != "All":
                df = df[df['Category'] == category_filter]
            
            # Display data with edit/delete options
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Edit/Delete section
            st.subheader("Edit or Delete Expense")
            expense_index = st.number_input("Enter expense index to edit/delete", min_value=0, max_value=len(df)-1)
            
            if expense_index < len(df):
                expense = df.iloc[expense_index]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_date = st.date_input("Date", value=pd.to_datetime(expense['Date']))
                    new_vendor = st.text_input("Vendor Name", value=expense['Vendor'])
                    new_category = st.selectbox(
                        "Category",
                        ["Travel", "Marketing", "Office Supplies", "Utilities", "Meals", "Other"],
                        index=["Travel", "Marketing", "Office Supplies", "Utilities", "Meals", "Other"].index(expense['Category'])
                    )
                    new_description = st.text_area("Description", value=expense.get('Description', ''))
                
                with col2:
                    new_amount = st.number_input("Amount", value=expense['Amount'], min_value=0.0, step=0.01)
                    new_payment_mode = st.selectbox(
                        "Payment Mode",
                        ["Cash", "UPI", "Bank Transfer", "Credit Card", "Other"],
                        index=["Cash", "UPI", "Bank Transfer", "Credit Card", "Other"].index(expense['Payment Mode'])
                    )
                    new_invoice_no = st.text_input("Invoice Number", value=expense['Invoice No'])

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Update Expense"):
                        tracker.update_expense(
                            expense_index,
                            new_date.strftime("%Y-%m-%d"),
                            new_vendor,
                            new_category,
                            new_amount,
                            new_payment_mode,
                            new_invoice_no,
                            new_description
                        )
                with col2:
                    if st.button("Delete Expense", type="secondary"):
                        tracker.delete_expense(expense_index)

    elif page == "Monthly Summary":
        st.header("Monthly Summary")
        
        monthly_summary = tracker.get_monthly_summary()
        
        if monthly_summary.empty:
            st.info("No expenses recorded yet!")
        else:
            # Display monthly summary
            st.bar_chart(monthly_summary)
            
            # Display table
            st.dataframe(
                monthly_summary.reset_index(),
                column_config={
                    "Date": "Month",
                    "Amount": st.column_config.NumberColumn(
                        "Total Amount",
                        format="₹%.2f"
                    )
                },
                hide_index=True
            )

    elif page == "Category Summary":
        st.header("Category Summary")
        
        category_summary = tracker.get_category_summary()
        
        if category_summary.empty:
            st.info("No expenses recorded yet!")
        else:
            # Display category summary
            st.bar_chart(category_summary)
            
            # Display table
            st.dataframe(
                category_summary.reset_index(),
                column_config={
                    "Category": "Category",
                    "Amount": st.column_config.NumberColumn(
                        "Total Amount",
                        format="₹%.2f"
                    )
                },
                hide_index=True
            )

    elif page == "Payment Summary":
        st.header("Payment Mode Summary")
        
        payment_summary = tracker.get_payment_summary()
        
        if payment_summary.empty:
            st.info("No expenses recorded yet!")
        else:
            # Display payment mode summary
            st.bar_chart(payment_summary)
            
            # Display table
            st.dataframe(
                payment_summary.reset_index(),
                column_config={
                    "Payment Mode": "Payment Mode",
                    "Amount": st.column_config.NumberColumn(
                        "Total Amount",
                        format="₹%.2f"
                    )
                },
                hide_index=True
            )

    elif page == "Export Data":
        st.header("Export Data")
        
        df = tracker.get_expenses()
        
        if df.empty:
            st.info("No expenses to export!")
        else:
            csv = tracker.export_to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="expenses.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main() 