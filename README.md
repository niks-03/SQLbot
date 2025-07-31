# SQLbot 🤖

A powerful Streamlit-based SQL chatbot that allows you to interact with your database using natural language queries. SQLbot leverages Google's Gemini AI to convert your questions into SQL queries and execute them against your MySQL database.

## 🚀 Features

### Core Functionality
- **Natural Language to SQL**: Ask questions in plain English and get SQL queries generated automatically
- **Database Management**: Create schemas and tables directly from the interface
- **Data Upload**: Upload CSV files to populate your tables
- **Real-time Query Execution**: Execute SQL queries and view results instantly
- **Interactive Chat Interface**: Modern chat-based UI for seamless interaction

### Database Operations
- **Schema Management**: Create and manage database schemas
- **Table Creation**: Build tables with custom column definitions
- **Data Import**: Bulk upload data from CSV files
- **Query Results**: View query results in formatted tables
- **Database Connection**: Secure connection management with credentials

### User Interface
- **Responsive Design**: Clean, modern interface built with Streamlit
- **Sidebar Navigation**: Easy access to all database operations
- **Popover Menus**: Organized functionality in collapsible sections
- **Real-time Feedback**: Success/error messages for all operations

## 📋 Prerequisites

Before running SQLbot, ensure you have:

- **Python 3.8+** installed on your system
- **MySQL Server** running and accessible
- **Google Gemini API Key** (free tier available)
- **Database credentials** (host, user, password)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SQLbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv myenv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   myenv\Scripts\activate
   
   # On macOS/Linux
   source myenv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### 1. Start the Application
```bash
streamlit run app.py
```

### 2. Initialize Credentials
1. Open the application in your browser
2. Click on "Initialize credentials" in the sidebar
3. Enter your credentials:
   - **Gemini API Key**: Your Google Gemini API key
   - **Database Host**: MySQL server host (e.g., localhost)
   - **Database User**: MySQL username
   - **Database Password**: MySQL password
4. Click "Initialize credentials"

### 3. Database Setup
1. **Select Schema**: Choose an existing schema or create a new one
2. **Select Table**: Choose an existing table or create a new one
3. **Create Schema** (if needed): Use the "Create schema" section in the sidebar
4. **Create Table** (if needed): Use the "create table" popover to define table structure

### 4. Data Management
1. **Upload Data**: Use the "upload data" popover to import CSV files
2. **Verify Data**: Check that your data is properly loaded
3. **Refresh Database**: Use the refresh button to update schema/table lists

### 5. Start Querying
1. **Ask Questions**: Type natural language questions in the chat input
2. **View Results**: See generated SQL and query results

## 📁 Project Structure

```
SQLbot/
├── app.py                 # Main Streamlit application
├── models/
│   ├── db_connection.py   # Database connection and operations
│   └── sql_model.py       # LLM integration and SQL generation
├── images/
│   └── sql.png           # Application logo
└── README.md             # This file
```

## 🔧 Configuration

### Database Requirements
- **MySQL Server**: Version 5.7 or higher recommended
- **User Permissions**: CREATE, SELECT, INSERT, DROP privileges
- **Network Access**: Ensure the database is accessible from your application

## 💡 Example Queries

Here are some example natural language queries you can try:

### Basic Queries
- "Show me all records from the users table"
- "How many customers do we have?"
- "What is the average age of our users?"

### Filtered Queries
- "Show me users who are older than 25"
- "Find all orders from last month"
- "Display products with price greater than $100"

### Aggregated Queries
- "What is the total revenue by month?"
- "Count the number of orders per customer"
- "Show me the top 10 customers by order value"

### Complex Queries
- "Find customers who have placed more than 5 orders"
- "Show me products that are out of stock but have pending orders"
- "Calculate the average order value for each customer segment"

## 🔄 Database Operations

### Creating Schemas
1. Enter schema name in the "Create schema" field
2. Click "Create schema"
3. Use the refresh button to see the new schema

### Creating Tables
1. Open the "create table" popover
2. Add columns with names and data types
3. Enter table name
4. Click "Create table"

### Uploading Data
1. Open the "upload data" popover
2. Select a CSV file
3. Choose target schema and table
4. Click "Upload to table"