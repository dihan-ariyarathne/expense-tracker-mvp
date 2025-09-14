# 💰 Personal Expense Tracker MVP

A simple web application for tracking personal income and expenses with analytics and charts.

## Features

- **User Authentication**: Sign up and login with email/password
- **Transaction Management**: Add income and expense transactions
- **Dashboard Overview**: 
  - Current balance (total income - total expenses)
  - Today's income and expense totals
  - Last transaction details
- **Analytics Charts**:
  - Pie chart showing expense categories (day/week/month view)
  - Line chart showing daily expense trends (week/month/year view)
- **Responsive Design**: Mobile-friendly interface

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the App**:
   Open your browser and go to `http://localhost:5000`

## Usage

1. **Sign Up**: Create a new account with your name, age, email, and password
2. **Login**: Use your email and password to access the dashboard
3. **Add Transactions**: Click "Add Transaction" to record income or expenses
4. **View Analytics**: Use the dashboard to see your financial overview and charts

## Transaction Categories

**Income Categories**: Salary, Gifts, Sales Revenue, Freelance, Investment, Other

**Expense Categories**: Food, Travel, Rent, Utilities, Entertainment, Healthcare, Shopping, Transportation, Other

## Technical Details

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5 + Chart.js
- **Security**: Password hashing with Werkzeug
- **Currency**: Sri Lankan Rupees (LKR)

## Database Schema

The application uses two main tables:
- `users`: Stores user account information
- `transactions`: Stores all income and expense records

## Environment Variables

Set `SECRET_KEY` environment variable for production:
```bash
export SECRET_KEY="your-secret-key-here"
```

## Development

The application runs in debug mode by default. For production deployment, ensure you:
1. Set a secure `SECRET_KEY`
2. Disable debug mode
3. Use a production WSGI server

## License

This project is for educational purposes.
