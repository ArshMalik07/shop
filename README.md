# Electronic Shop Management System using Flask

# Project Overview
This project is a Flask web application for managing a shop's inventory, sales, and customer records. It connects to a MySQL database and provides functionalities for adding items, processing sales, and generating reports.

## Prerequisites
- Python 3.x
- MySQL server setup

## Installation Steps
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup
- Create a MySQL database named `shop`.
- The application will create necessary tables on the first run.

## Running the Application
- Use the command:
   ```bash
   gunicorn app:app
   ```
- Access the application in a web browser at `http://localhost:8000`.

## Usage
- Login to the application.
- Add items to the inventory.
- Process sales and generate reports.


