import sqlite3
from datetime import datetime, timedelta
import random

# Sample data for realistic expense tracking
income_categories = ['Salary', 'Gifts', 'Sales Revenue', 'Freelance', 'Investment']
expense_categories = ['Food', 'Travel', 'Rent', 'Utilities', 'Entertainment', 'Healthcare', 'Shopping', 'Transportation']

# Sample transaction data
sample_transactions = [
    # Income transactions
    {'type': 'income', 'category': 'Salary', 'amount': 150000.00, 'note': 'Monthly salary'},
    {'type': 'income', 'category': 'Freelance', 'amount': 25000.00, 'note': 'Web development project'},
    {'type': 'income', 'category': 'Gifts', 'amount': 5000.00, 'note': 'Birthday gift from family'},
    
    # Food expenses (multiple entries)
    {'type': 'expense', 'category': 'Food', 'amount': 2500.00, 'note': 'Grocery shopping'},
    {'type': 'expense', 'category': 'Food', 'amount': 1200.00, 'note': 'Lunch at restaurant'},
    {'type': 'expense', 'category': 'Food', 'amount': 450.00, 'note': 'Coffee and pastry'},
    {'type': 'expense', 'category': 'Food', 'amount': 3500.00, 'note': 'Weekly groceries'},
    {'type': 'expense', 'category': 'Food', 'amount': 2800.00, 'note': 'Dinner with friends'},
    {'type': 'expense', 'category': 'Food', 'amount': 800.00, 'note': 'Fast food lunch'},
    {'type': 'expense', 'category': 'Food', 'amount': 2200.00, 'note': 'Weekend brunch'},
    {'type': 'expense', 'category': 'Food', 'amount': 1500.00, 'note': 'Takeout dinner'},
    {'type': 'expense', 'category': 'Food', 'amount': 1800.00, 'note': 'Grocery store'},
    {'type': 'expense', 'category': 'Food', 'amount': 900.00, 'note': 'Office lunch'},
    
    # Transportation expenses
    {'type': 'expense', 'category': 'Transportation', 'amount': 8000.00, 'note': 'Gas fill-up'},
    {'type': 'expense', 'category': 'Transportation', 'amount': 500.00, 'note': 'Uber ride'},
    {'type': 'expense', 'category': 'Transportation', 'amount': 150.00, 'note': 'Public transport'},
    {'type': 'expense', 'category': 'Transportation', 'amount': 6000.00, 'note': 'Gas station'},
    {'type': 'expense', 'category': 'Transportation', 'amount': 300.00, 'note': 'Parking fee'},
    {'type': 'expense', 'category': 'Transportation', 'amount': 800.00, 'note': 'Taxi ride'},
    
    # Entertainment expenses
    {'type': 'expense', 'category': 'Entertainment', 'amount': 1200.00, 'note': 'Netflix subscription'},
    {'type': 'expense', 'category': 'Entertainment', 'amount': 2000.00, 'note': 'Movie tickets'},
    {'type': 'expense', 'category': 'Entertainment', 'amount': 3500.00, 'note': 'Concert ticket'},
    {'type': 'expense', 'category': 'Entertainment', 'amount': 800.00, 'note': 'Spotify Premium'},
    {'type': 'expense', 'category': 'Entertainment', 'amount': 2500.00, 'note': 'Bowling with friends'},
    
    # Shopping expenses
    {'type': 'expense', 'category': 'Shopping', 'amount': 3500.00, 'note': 'New shirt'},
    {'type': 'expense', 'category': 'Shopping', 'amount': 8500.00, 'note': 'Online purchase'},
    {'type': 'expense', 'category': 'Shopping', 'amount': 2500.00, 'note': 'Books'},
    {'type': 'expense', 'category': 'Shopping', 'amount': 15000.00, 'note': 'Electronics'},
    {'type': 'expense', 'category': 'Shopping', 'amount': 1800.00, 'note': 'Household items'},
    
    # Utilities
    {'type': 'expense', 'category': 'Utilities', 'amount': 8500.00, 'note': 'Electricity bill'},
    {'type': 'expense', 'category': 'Utilities', 'amount': 1200.00, 'note': 'Water bill'},
    {'type': 'expense', 'category': 'Utilities', 'amount': 3500.00, 'note': 'Internet bill'},
    {'type': 'expense', 'category': 'Utilities', 'amount': 2500.00, 'note': 'Phone bill'},
    
    # Healthcare
    {'type': 'expense', 'category': 'Healthcare', 'amount': 1200.00, 'note': 'Pharmacy'},
    {'type': 'expense', 'category': 'Healthcare', 'amount': 5000.00, 'note': 'Doctor visit'},
    {'type': 'expense', 'category': 'Healthcare', 'amount': 1800.00, 'note': 'Prescription medication'},
    
    # Travel
    {'type': 'expense', 'category': 'Travel', 'amount': 15000.00, 'note': 'Weekend trip'},
    {'type': 'expense', 'category': 'Travel', 'amount': 12000.00, 'note': 'Hotel booking'},
    {'type': 'expense', 'category': 'Travel', 'amount': 2500.00, 'note': 'Train ticket'},
    
    # Rent (if applicable)
    {'type': 'expense', 'category': 'Rent', 'amount': 45000.00, 'note': 'Monthly rent'},
]

def add_sample_data():
    # Connect to database
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    # Get the first user (assuming you have one)
    cursor.execute('SELECT id FROM users LIMIT 1')
    user = cursor.fetchone()
    
    if not user:
        print("No users found. Please create an account first.")
        return
    
    user_id = user[0]
    
    # Add transactions over the past month
    today = datetime.now()
    
    for i, transaction in enumerate(sample_transactions):
        # Spread transactions over the past 30 days
        days_ago = random.randint(0, 30)
        transaction_date = today - timedelta(days=days_ago)
        
        # Add some randomness to the time
        hour = random.randint(8, 22)
        minute = random.randint(0, 59)
        transaction_date = transaction_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        cursor.execute('''
            INSERT INTO transactions (user_id, t_type, category, amount, note, ts, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            transaction['type'],
            transaction['category'],
            transaction['amount'],
            transaction['note'],
            transaction_date,
            transaction_date
        ))
    
    conn.commit()
    conn.close()
    
    print(f"Added {len(sample_transactions)} sample transactions for the past month!")
    print("You can now view the dashboard to see the visualizations.")

if __name__ == '__main__':
    add_sample_data()
