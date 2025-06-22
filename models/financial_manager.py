import json
import os
from .profile import Profile

class FinancialManager:
    """Class to manage multiple user profiles and data persistence"""
    
    def __init__(self, data_file='data/financial_data.json'):
        self.data_file = data_file
        self.profiles = []
        self.ensure_data_directory()
        self.load_data()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def add_profile(self, profile):
        """Add a new profile"""
        if isinstance(profile, Profile):
            # Check if profile name already exists
            existing_names = [p.name for p in self.profiles]
            if profile.name not in existing_names:
                self.profiles.append(profile)
                self.save_data()
                return True
            else:
                raise ValueError(f"Profile with name '{profile.name}' already exists")
        else:
            raise ValueError("Profile must be an instance of Profile class")
    
    def get_profile(self, name):
        """Get a profile by name"""
        for profile in self.profiles:
            if profile.name == name:
                return profile
        return None
    
    def remove_profile(self, name):
        """Remove a profile by name"""
        profile = self.get_profile(name)
        if profile:
            self.profiles.remove(profile)
            self.save_data()
            return True
        return False
    
    def get_all_profiles(self):
        """Get all profiles"""
        return self.profiles.copy()
    
    def save_data(self):
        """Save all profiles to JSON file"""
        try:
            data = {
                'profiles': [profile.to_dict() for profile in self.profiles]
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load profiles from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                self.profiles = []
                for profile_data in data.get('profiles', []):
                    profile = Profile.from_dict(profile_data)
                    self.profiles.append(profile)
                    
        except Exception as e:
            print(f"Error loading data: {e}")
            self.profiles = []
    
    def get_summary_statistics(self):
        """Get summary statistics for all profiles"""
        total_profiles = len(self.profiles)
        total_transactions = sum(profile.get_transaction_count() for profile in self.profiles)
        total_balance = sum(profile.get_balance() for profile in self.profiles)
        
        return {
            'total_profiles': total_profiles,
            'total_transactions': total_transactions,
            'total_balance': total_balance
        }
    
    def backup_data(self, backup_file=None):
        """Create a backup of the data"""
        if backup_file is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"data/backup_financial_data_{timestamp}.json"
        
        try:
            data = {
                'profiles': [profile.to_dict() for profile in self.profiles]
            }
            
            with open(backup_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            
            return backup_file
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
    
    def __str__(self):
        """String representation of financial manager"""
        stats = self.get_summary_statistics()
        return f"Financial Manager - Profiles: {stats['total_profiles']}, Transactions: {stats['total_transactions']}, Total Balance: Rp {stats['total_balance']:,.2f}"