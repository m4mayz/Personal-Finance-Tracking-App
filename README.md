# Personal Finance Tracker

## Inspiration

This app was inspired by my personal experience in managing my finances as a student. It was often difficult for me to keep track of my daily income and expenses, especially when it came to sharing financial information with my parents or monitoring my spending habits. I realized that manual recording in a book or cellphone notepad is often forgotten and not well organized.

From this problem, I wanted to create an application that allows multiple profiles (for example for families) where each person can record their own financial transactions with a user-friendly interface. This application also provides real-time balance visualization and transaction history that makes it easy to track personal finances.

## Features

-   **Multi-Profile Management**: Create and manage multiple user profiles
-   **Transaction Recording**: Record income and expenses with descriptions
-   **Real-time Balance Tracking**: View current balance with color-coded display
-   **Transaction History**: Complete history of all transactions with timestamps
-   **Data Persistence**: Automatic data saving in JSON format
-   **User-friendly GUI**: Clean and intuitive graphical interface
-   **Currency Support**: Indonesian Rupiah (IDR) formatting

## Installation & Setup

### Prerequisites

-   Python 3.7 or higher
-   tkinter (usually included with Python)

### Installation Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/m4mayz/Personal-Finance-Tracking-App.git
    cd Personal-Finance-Tracking-App
    ```

2. **Ensure Python is installed**:

    ```bash
    python --version
    ```

3. **No additional packages required** - uses only Python standard library

## How to Run

1. **Navigate to project directory**:

    ```bash
    cd Personal-Finance-Tracking-App
    ```

2. **Run the application**:

    ```bash
    python main.py
    ```

3. **First time usage**:
    - Click "New Profile" to create your first profile
    - Enter your name and click "Create"
    - Select your profile from the dropdown
    - Start adding transactions!

## Usage Guide

### Creating a Profile

1. Click the "New Profile" button
2. Enter your name in the dialog box
3. Click "Create" or press Enter

### Adding Transactions

1. Select your profile from the dropdown menu
2. Choose transaction type (Income/Expense)
3. Enter a description for the transaction
4. Enter the amount in Rupiah
5. Click "Add Transaction"

### Viewing Transaction History

-   All transactions are displayed in the history table
-   Shows date, type, description, amount, and running balance
-   Income transactions are marked with "+"
-   Expense transactions are marked with "-"

### Balance Display

-   Current balance is displayed prominently at the top
-   Green background for positive balance
-   Red background for negative balance
-   Real-time updates after each transaction

## Data Storage

-   Data is automatically saved in JSON format
-   File location: `data/financial_data.json`
-   Backup functionality available through FinancialManager class
-   Data includes:
    -   Profile information
    -   Transaction history with timestamps
    -   Automatic data recovery on application restart

## Demo Video (Youtube)

[![Watch the demo](https://img.youtube.com/vi/Skxm2a5SdRI/0.jpg)](https://www.youtube.com/watch?v=Skxm2a5SdRI)

## Author

Akmal Zaidan Hibatullah | NIM.20230040065

Developed as part of Object-Oriented Programming course assignment.

## License

This project is for educational purposes only.
