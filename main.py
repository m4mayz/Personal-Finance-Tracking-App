import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from models.transaction import Transaction, Income, Expense
from models.profile import Profile
from models.financial_manager import FinancialManager

class PersonalFinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Center the main window
        self.center_window(self.root, 800, 600)
        
        # Make main window non-resizable for better layout control
        self.root.resizable(True, True)
        self.root.minsize(750, 550)  # Set minimum size
        
        # Initialize financial manager
        self.financial_manager = FinancialManager()
        self.current_profile = None
        
        # Create main frames
        self.create_widgets()
        self.load_profiles()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Personal Finance Tracker", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Profile selection frame
        profile_frame = tk.Frame(self.root, bg='#f0f0f0')
        profile_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(profile_frame, text="Select Profile:", font=("Arial", 10), bg='#f0f0f0').pack(side='left')
        
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(profile_frame, textvariable=self.profile_var, 
                                         state="readonly", width=20)
        self.profile_combo.pack(side='left', padx=10)
        self.profile_combo.bind('<<ComboboxSelected>>', self.on_profile_selected)
        
        # Buttons for profile management
        tk.Button(profile_frame, text="New Profile", command=self.create_new_profile,
                 bg='#4CAF50', fg='white', font=("Arial", 9)).pack(side='left', padx=5)
        
        # Balance display
        self.balance_frame = tk.Frame(self.root, bg='#e8f5e8', relief='raised', bd=2)
        self.balance_frame.pack(pady=10, padx=20, fill='x')
        
        self.balance_label = tk.Label(self.balance_frame, text="Current Balance: Rp 0", 
                                     font=("Arial", 14, "bold"), bg='#e8f5e8')
        self.balance_label.pack(pady=10)
        
        # Transaction input frame
        input_frame = tk.LabelFrame(self.root, text="Add New Transaction", 
                                   font=("Arial", 12, "bold"), bg='#f0f0f0')
        input_frame.pack(pady=10, padx=20, fill='x')
        
        # Transaction type selection
        type_frame = tk.Frame(input_frame, bg='#f0f0f0')
        type_frame.pack(pady=5, fill='x')
        
        tk.Label(type_frame, text="Type:", font=("Arial", 10), bg='#f0f0f0').pack(side='left')
        
        self.transaction_type = tk.StringVar(value="Income")
        tk.Radiobutton(type_frame, text="Income", variable=self.transaction_type, 
                      value="Income", bg='#f0f0f0', font=("Arial", 9)).pack(side='left', padx=10)
        tk.Radiobutton(type_frame, text="Expense", variable=self.transaction_type, 
                      value="Expense", bg='#f0f0f0', font=("Arial", 9)).pack(side='left', padx=10)
        
        # Description input
        desc_frame = tk.Frame(input_frame, bg='#f0f0f0')
        desc_frame.pack(pady=5, fill='x')
        
        tk.Label(desc_frame, text="Description:", font=("Arial", 10), bg='#f0f0f0').pack(side='left')
        self.description_entry = tk.Entry(desc_frame, font=("Arial", 10), width=30)
        self.description_entry.pack(side='left', padx=10)
        
        # Amount input
        amount_frame = tk.Frame(input_frame, bg='#f0f0f0')
        amount_frame.pack(pady=5, fill='x')
        
        tk.Label(amount_frame, text="Amount (Rp):", font=("Arial", 10), bg='#f0f0f0').pack(side='left')
        self.amount_entry = tk.Entry(amount_frame, font=("Arial", 10), width=20)
        self.amount_entry.pack(side='left', padx=10)
        
        # Add transaction button
        tk.Button(input_frame, text="Add Transaction", command=self.add_transaction,
                 bg='#2196F3', fg='white', font=("Arial", 10, "bold")).pack(pady=10)
        
        # Transaction history frame
        history_frame = tk.LabelFrame(self.root, text="Transaction History", 
                                     font=("Arial", 12, "bold"), bg='#f0f0f0')
        history_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Treeview for displaying transactions
        columns = ('Date', 'Type', 'Description', 'Amount', 'Balance')
        self.transaction_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=120, anchor='center')
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transaction_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initially disable transaction inputs
        self.toggle_transaction_inputs(False)
    
    def center_window(self, window, width, height):
        """Center a window on the screen"""
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position coordinates
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window position
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_message(self, title, message, msg_type="info"):
        """Show centered message dialog"""
        if msg_type == "error":
            messagebox.showerror(title, message, parent=self.root)
        elif msg_type == "warning":
            messagebox.showwarning(title, message, parent=self.root)
        else:
            messagebox.showinfo(title, message, parent=self.root)
        
    def create_new_profile(self):
        """Create a new user profile"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Profile")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog_width = 350
        dialog_height = 180
        self.center_window(dialog, dialog_width, dialog_height)
        
        # Make dialog non-resizable
        dialog.resizable(False, False)
        
        # Set dialog icon (same as main window)
        try:
            dialog.iconbitmap(self.root.iconbitmap())
        except:
            pass  # Ignore if no icon is set
        
        tk.Label(dialog, text="Enter your name:", font=("Arial", 12), bg='#f0f0f0').pack(pady=15)
        
        name_entry = tk.Entry(dialog, font=("Arial", 11), width=25)
        name_entry.pack(pady=8)
        name_entry.focus()
        
        def save_profile():
            name = name_entry.get().strip()
            if name:
                if name not in [profile.name for profile in self.financial_manager.profiles]:
                    profile = Profile(name)
                    self.financial_manager.add_profile(profile)
                    self.load_profiles()
                    self.profile_var.set(name)
                    self.on_profile_selected()
                    dialog.destroy()
                else:
                    self.show_message("Error", "Profile name already exists!", "error")
            else:
                self.show_message("Error", "Please enter a valid name!", "error")
        
        tk.Button(dialog, text="Create", command=save_profile,
                 bg='#4CAF50', fg='white', font=("Arial", 10, "bold")).pack(pady=15)
        
        tk.Button(dialog, text="Cancel", command=dialog.destroy,
                 bg='#f44336', fg='white', font=("Arial", 10)).pack(pady=(0, 10))
        
        # Bind Enter key to save
        dialog.bind('<Return>', lambda e: save_profile())
        
    def load_profiles(self):
        """Load existing profiles into combobox"""
        profile_names = [profile.name for profile in self.financial_manager.profiles]
        self.profile_combo['values'] = profile_names
        
    def on_profile_selected(self, event=None):
        """Handle profile selection"""
        selected_name = self.profile_var.get()
        if selected_name:
            self.current_profile = self.financial_manager.get_profile(selected_name)
            if self.current_profile:
                self.toggle_transaction_inputs(True)
                self.update_display()
            
    def toggle_transaction_inputs(self, enabled):
        """Enable or disable transaction input widgets"""
        state = 'normal' if enabled else 'disabled'
        self.description_entry.config(state=state)
        self.amount_entry.config(state=state)
        
    def add_transaction(self):
        """Add a new transaction"""
        if not self.current_profile:
            self.show_message("Error", "Please select a profile first!", "error")
            return
            
        description = self.description_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        
        if not description or not amount_str:
            self.show_message("Error", "Please fill in all fields!", "error")
            return
            
        try:
            amount = float(amount_str)
            if amount <= 0:
                self.show_message("Error", "Amount must be positive!", "error")
                return
        except ValueError:
            self.show_message("Error", "Please enter a valid number for amount!", "error")
            return
            
        # Create transaction based on type
        transaction_type = self.transaction_type.get()
        if transaction_type == "Income":
            transaction = Income(description, amount)
        else:
            transaction = Expense(description, amount)
            
        # Add transaction to current profile
        self.current_profile.add_transaction(transaction)
        
        # Save data
        self.financial_manager.save_data()
        
        # Clear inputs
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        
        # Update display
        self.update_display()
        
        self.show_message("Success", f"{transaction_type} added successfully!")
        
    def update_display(self):
        """Update balance and transaction history display"""
        if not self.current_profile:
            return
            
        # Update balance
        balance = self.current_profile.get_balance()
        self.balance_label.config(text=f"Current Balance: Rp {balance:,.2f}")
        
        # Update balance color based on value
        if balance >= 0:
            self.balance_frame.config(bg='#e8f5e8')
            self.balance_label.config(bg='#e8f5e8', fg='#2e7d32')
        else:
            self.balance_frame.config(bg='#ffebee')
            self.balance_label.config(bg='#ffebee', fg='#c62828')
        
        # Clear existing items
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
            
        # Add transactions to treeview
        running_balance = 0
        for transaction in self.current_profile.transactions:
            running_balance += transaction.get_amount()
            
            # Format date
            date_str = transaction.date.strftime("%Y-%m-%d %H:%M")
            
            # Format amount with color coding
            amount_str = f"Rp {abs(transaction.amount):,.2f}"
            
            # Insert into treeview
            item = self.transaction_tree.insert('', 'end', values=(
                date_str,
                transaction.get_type(),
                transaction.description,
                amount_str,
                f"Rp {running_balance:,.2f}"
            ))
            
            # Color coding for different transaction types
            if isinstance(transaction, Income):
                self.transaction_tree.set(item, 'Type', '+ Income')
            else:
                self.transaction_tree.set(item, 'Type', '- Expense')
    
    def on_closing(self):
        """Handle application closing"""
        try:
            # Save data before closing
            if self.financial_manager:
                self.financial_manager.save_data()
        except Exception as e:
            print(f"Error saving data on close: {e}")
        finally:
            self.root.destroy()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = PersonalFinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()