from flask import Flask, render_template, request, redirect, session, send_file,jsonify
import mysql.connector
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import fonts
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PyPDF2 import PdfMerger
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import base64

pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/DejaVuSans.ttf'))
import os
from reportlab.pdfbase.ttfonts import TTFont

# Get the absolute path of the font file
base_path = os.path.dirname(__file__)
font_path = os.path.join(base_path, 'static', 'DejaVuSans.ttf')

# Register the font
pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))




app = Flask(__name__)
app.secret_key = '#1109#'

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12741524",
    password="ieEZMNMzDq",
    database="sql12741524"
)

# Create users table if not exists
def create_users_table():
    cursor = mydb.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, unique_code VARCHAR(255))")
    mydb.commit()

create_users_table()

# Create items table if not exists
def create_items_table():
    cursor = mydb.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, quantity INT NOT NULL, user_id INT, unique_code VARCHAR(20))")
    mydb.commit()

create_items_table()

def create_sales_table():
    cursor = mydb.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            item_code VARCHAR(255),
            item_name VARCHAR(255),
            customer_name VARCHAR(255),
            quantity INT,
            amount DECIMAL(10, 2),
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    mydb.commit()

create_sales_table()





@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    message = ""
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            item_name = request.form['item_name']
            quantity = int(request.form['quantity'])
            unique_code = request.form['unique_code']

            cursor = mydb.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cursor.fetchone()[0]

            # Check if item already exists for the user
            cursor.execute("SELECT id, quantity FROM items WHERE user_id = %s AND unique_code = %s", (user_id, unique_code))
            item = cursor.fetchone()

            if item:
                # Item exists, update the quantity
                new_quantity = item[1] + quantity
                cursor.execute("UPDATE items SET quantity = %s WHERE id = %s", (new_quantity, item[0]))
                message = "Item quantity updated successfully!"
            else:
                # Item does not exist, insert new item
                sql = "INSERT INTO items (name, quantity, user_id, unique_code) VALUES (%s, %s, %s, %s)"
                val = (item_name, quantity, user_id, unique_code)
                cursor.execute(sql, val)
                message = "Item added successfully!"

            mydb.commit()
            cursor.close()

    return render_template('add_item.html', message=message)


@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if 'username' in session:
        username = session['username']
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        cursor.close()  # Close the cursor after fetching the user_id

        if request.method == 'POST':
            items = request.form.getlist('item')
            quantities = request.form.getlist('quantity')
            amounts = request.form.getlist('amount')
            customer_name = request.form['customer_name']

            if items and quantities and amounts:
                total_amount = 0
                pdf_data = []
                merger = PdfMerger()  # Create PdfMerger instance

                for i in range(len(items)):
                    item_code = items[i]
                    quantity = int(quantities[i])
                    amount = float(amounts[i])
                    total_amount += quantity * amount

                    cursor = mydb.cursor()
                    cursor.execute("SELECT id, name, quantity FROM items WHERE unique_code = %s AND user_id = %s", (item_code, user_id))
                    item = cursor.fetchone()
                    cursor.close()  # Close the cursor after fetching the item

                    if item and item[2] >= quantity:
                        item_id = item[0]
                        item_name = item[1]

                        cursor = mydb.cursor()
                        sql = "INSERT INTO sales (user_id, item_code, item_name, customer_name, quantity, amount) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = (user_id, item_code, item_name, customer_name, quantity, amount)
                        cursor.execute(sql, val)
                        mydb.commit()

                        new_quantity = item[2] - quantity
                        cursor.execute("UPDATE items SET quantity = %s WHERE id = %s", (new_quantity, item_id))
                        mydb.commit()
                        cursor.close()  
                        # pdf_data.append([item_code, item_name, quantity, amount, quantity * amount])

                        # Append to PDF
                        merger.append(io.BytesIO(generate_pdf(customer_name, item_code, item_name, quantity, amount).getvalue()))

                    else:
                        message = "Item not available or insufficient quantity."
                        return render_template('billing.html', message=message)

                # Save merged PDF
                output_pdf = io.BytesIO()
                merger.write(output_pdf)
                output_pdf.seek(0)

                return send_file(
                    output_pdf,
                    as_attachment=False,
                    mimetype='application/pdf',
                    download_name='bill.pdf'
                )

            else:
                message = "Please add items."
                return render_template('billing.html', message=message)
        else:
            message = ""

        cursor = mydb.cursor()
        cursor.execute("SELECT name, unique_code, quantity FROM items WHERE user_id = %s", (user_id,))
        items = cursor.fetchall()
        cursor.close()  # Close the cursor after fetching the items

        return render_template('billing.html', items=items, message=message)
    else:
        return redirect('/login')



def generate_pdf(customer_name, item_code, item_name, quantity, amount):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Set DejaVu Sans font
    c.setFont("DejaVuSans", 12)

    # Register and set DejaVuSans-Bold font
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path))
    c.setFont("DejaVuSans-Bold", 24)

    # PDF Title
    c.drawCentredString(width / 2.0, height - 40, "Billing Invoice")

    # Current Date
    current_date = datetime.now().strftime("%Y-%m-%d")  # Format the date
    c.setFont("DejaVuSans", 12)
    c.drawString(50, height - 80, f"Date: {current_date}")

    # Customer Information
    c.setFont("DejaVuSans", 12)
    c.drawString(50, height - 100, f"Customer Name: {customer_name}")

    # Item Information
    c.drawString(50, height - 140, f"Item Code: {item_code}")
    c.drawString(50, height - 160, f"Item Name: {item_name}")
    c.drawString(50, height - 180, f"Quantity: {quantity}")
    c.drawString(50, height - 200, f"Amount(per item): ₹{amount:.2f}")

    # Total
    total_amount = quantity * amount
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(50, height - 240, f"Total: ₹{total_amount:.2f}")

    c.showPage()
    c.save()
    buffer.seek(0)

    return buffer


    

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if 'username' in session:
        username = session['username']
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        
        search_query = ""
        if request.method == 'POST':
            search_query = request.form['search']

        # Calculate date one year ago
        one_year_ago = datetime.now() - timedelta(days=365)

        # Use search query if provided, otherwise fetch all records within the past year
        if search_query:
            cursor.execute("""
                SELECT item_name, customer_name, quantity, amount, sale_date 
                FROM sales 
                WHERE user_id = %s AND customer_name LIKE %s AND sale_date >= %s
                           ORDER BY sale_date DESC
            """, (user_id, '%' + search_query + '%', one_year_ago))
        else:
            cursor.execute("""
                SELECT item_name, customer_name, quantity, amount, sale_date 
                FROM sales 
                WHERE user_id = %s AND sale_date >= %s
                           ORDER BY sale_date DESC
            """, (user_id, one_year_ago))
        
        sales_records = cursor.fetchall()
        
        return render_template('customers.html', sales_records=sales_records, search_query=search_query)
    else:
        return redirect('/login')
    

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect('/login')
    

@app.route('/delete_item', methods=['POST'])
def delete_item():
    if 'username' in session:
        username = session['username']
        unique_code = request.form['unique_code']
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        sql = "DELETE FROM items WHERE user_id = %s AND unique_code = %s"
        val = (user_id, unique_code)
        cursor.execute(sql, val)
        mydb.commit()
        return redirect('/stock')
    else:
        return redirect('/login')
    
def delete_zero_quantity_items(user_id):
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM items WHERE user_id = %s AND quantity = 0", (user_id,))
    mydb.commit()
    cursor.close()

    

@app.route('/reports')
def generate_reports():
    if 'username' in session:
        username = session['username']
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        
        # Fetch items with present quantity and sold quantity
        cursor.execute("""
            SELECT i.name, COALESCE(SUM(s.quantity), 0) AS sold_quantity, COALESCE(SUM(i.quantity), 0) AS present_quantity
            FROM items i
            LEFT JOIN sales s ON i.unique_code = s.item_code
            WHERE i.user_id = %s
            GROUP BY i.name
        """, (user_id,))
        
        results = cursor.fetchall()
        item_names = []
        sold_quantities = []
        available_quantities = []

        for row in results:
            item_names.append(row[0])
            sold_quantities.append(row[1])
            available_quantities.append(row[2])

        # Plotting using bar graph
        plt.figure(figsize=(12, 6))
        x = range(len(item_names))
        plt.bar(x, available_quantities, width=0.4, label='Available Quantity', color='green', align='center')
        plt.bar(x, sold_quantities, width=0.4, label='Sold Quantity', color='blue', align='edge')

        plt.xlabel('Items')
        plt.ylabel('Quantity')
        plt.title('Sales and Available Quantities')
        plt.xticks(x, item_names, rotation=45)
        plt.legend()
        plt.tight_layout()

        # Save plot to a BytesIO object
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)  # Go back to the beginning of the buffer

        # Encode the plot buffer to base64
        plot_url = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return render_template('reports.html', plot_url=plot_url)

    else:
        return redirect('/login')

    
@app.route('/')
def home_page():
    return render_template('login.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        val = (username, password)
        cursor.execute(sql, val)
        user = cursor.fetchone()
        if user:
            session['username'] = user[1]
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect('/login')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        cursor.execute(sql, val)
        mydb.commit()
        return redirect('/login')  # Redirect to login page after registration
    return render_template('register.html')






@app.route('/records', methods=['GET', 'POST'])
def records():
    if 'username' in session:
        username = session['username']
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        
        # Calculate date one year ago
        one_year_ago = datetime.now() - timedelta(days=365)
        
        if request.method == 'POST':
            search_query = request.form['search']
            cursor.execute("""
                SELECT item_code, item_name, customer_name, quantity, amount, sale_date 
                FROM sales 
                WHERE user_id = %s AND customer_name LIKE %s AND sale_date >= %s
                           ORDER BY sale_date DESC
            """, (user_id, '%' + search_query + '%', one_year_ago))
        else:
            cursor.execute("""
                SELECT item_code, item_name, customer_name, quantity, amount, sale_date 
                FROM sales WHERE user_id = %s AND sale_date >= %s
                           ORDER BY sale_date DESC
            """, (user_id, one_year_ago))
        
        sales_records = cursor.fetchall()
        
        return render_template('records.html', sales_records=sales_records)
    else:
        return redirect('/login')
    

@app.route('/search', methods=['GET'])
def search():
    if 'username' in session:
        username = session['username']
        search_query = request.args.get('search')
        
        if search_query:
            try:
                cursor = mydb.cursor()
                query = """
                SELECT name, quantity, unique_code 
                FROM items 
                WHERE user_id = (SELECT id FROM users WHERE username = %s) 
                AND unique_code = %s
                """
                cursor.execute(query, (username, search_query))
                items = cursor.fetchall()
                
                # Debugging prints
                print(f"Search Query: {search_query}")
                print(f"Items Found: {items}")
                
                return render_template('stock.html', items=items)
            except Exception as e:
                print(f"An error occurred: {e}")
                return render_template('stock.html', items=[], error="An error occurred while searching.")
        else:
            # Handle case where search_query is empty
            print("Search query is empty.")
            return render_template('stock.html', items=[], error="Please enter a search query.")
    else:
        return redirect('/login')




@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if 'username' in session:
        username = session['username']
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]

        # Check if a search query was submitted
        item_name = request.args.get('itemname')
        if item_name:
            search_query = f"%{item_name}%"  # Ensure that the wildcard search is properly formatted
            cursor.execute("SELECT name, quantity, unique_code FROM items WHERE user_id = %s AND name LIKE %s", (user_id, search_query))
        else:
            cursor.execute("SELECT name, quantity, unique_code FROM items WHERE user_id = %s ORDER BY name", (user_id,))
        
        items = cursor.fetchall()

        # Check if the request is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            items_list = [{'name': item[0], 'quantity': item[1], 'unique_code': item[2]} for item in items]
            return jsonify(items=items_list)
        else:
            return render_template('stock.html', items=items)
    else:
        return redirect('/login')





    

if __name__ == '__main__':
    app.run(debug=True)
