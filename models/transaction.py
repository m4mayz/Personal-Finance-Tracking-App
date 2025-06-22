from abc import ABC, abstractmethod
from datetime import datetime
import json

class Transaction(ABC):
    """Abstract base class for all transactions"""
    
    def __init__(self, description, amount):
        self.description = description
        self.amount = abs(amount)  # Store absolute value
        self.date = datetime.now()
        
    @abstractmethod
    def get_amount(self):
        """Get the transaction amount with appropriate sign"""
        pass
    
    @abstractmethod
    def get_type(self):
        """Get the transaction type as string"""
        pass
    
    def to_dict(self):
        """Convert transaction to dictionary for JSON serialization"""
        return {
            'type': self.get_type(),
            'description': self.description,
            'amount': self.amount,
            'date': self.date.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        """Create transaction from dictionary"""
        transaction_type = data['type']
        description = data['description']
        amount = data['amount']
        date_str = data['date']
        
        if transaction_type == 'Income':
            transaction = Income(description, amount)
        else:
            transaction = Expense(description, amount)
            
        # Restore the original date
        transaction.date = datetime.fromisoformat(date_str)
        return transaction
    
    def __str__(self):
        """String representation of transaction"""
        return f"{self.get_type()}: {self.description} - Rp {self.amount:,.2f} ({self.date.strftime('%Y-%m-%d %H:%M')})"

class Income(Transaction):
    """Class representing income transactions"""
    
    def get_amount(self):
        """Income returns positive amount"""
        return self.amount
    
    def get_type(self):
        """Return transaction type"""
        return "Income"

class Expense(Transaction):
    """Class representing expense transactions"""
    
    def get_amount(self):
        """Expense returns negative amount"""
        return -self.amount
    
    def get_type(self):
        """Return transaction type"""
        return "Expense"