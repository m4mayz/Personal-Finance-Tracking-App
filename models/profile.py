from datetime import datetime
from .transaction import Transaction

class Profile:
    """Class representing a user profile with their financial transactions"""
    
    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.created_date = datetime.now()
    
    def add_transaction(self, transaction):
        """Add a transaction to the profile"""
        if isinstance(transaction, Transaction):
            self.transactions.append(transaction)
        else:
            raise ValueError("Transaction must be an instance of Transaction class")
    
    def get_balance(self):
        """Calculate and return current balance"""
        balance = 0
        for transaction in self.transactions:
            balance += transaction.get_amount()
        return balance
    
    def get_total_income(self):
        """Calculate total income"""
        total_income = 0
        for transaction in self.transactions:
            if transaction.get_type() == "Income":
                total_income += transaction.amount
        return total_income
    
    def get_total_expenses(self):
        """Calculate total expenses"""
        total_expenses = 0
        for transaction in self.transactions:
            if transaction.get_type() == "Expense":
                total_expenses += transaction.amount
        return total_expenses
    
    def get_transaction_count(self):
        """Get total number of transactions"""
        return len(self.transactions)
    
    def get_recent_transactions(self, count=5):
        """Get most recent transactions"""
        return self.transactions[-count:] if count <= len(self.transactions) else self.transactions
    
    def to_dict(self):
        """Convert profile to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'created_date': self.created_date.isoformat(),
            'transactions': [transaction.to_dict() for transaction in self.transactions]
        }
    
    @staticmethod
    def from_dict(data):
        """Create profile from dictionary"""
        profile = Profile(data['name'])
        profile.created_date = datetime.fromisoformat(data['created_date'])
        
        # Load transactions
        for transaction_data in data['transactions']:
            transaction = Transaction.from_dict(transaction_data)
            profile.transactions.append(transaction)
            
        return profile
    
    def __str__(self):
        """String representation of profile"""
        return f"Profile: {self.name} - Balance: Rp {self.get_balance():,.2f} - Transactions: {len(self.transactions)}"