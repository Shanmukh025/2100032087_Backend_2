from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_customers')
def list_customers():
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers")
        customers = cursor.fetchall()
        conn.close()
        print(customers)
    return render_template('customers.html', customers=customers)

@app.route('/orders_january_2023')
def orders_january_2023():
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders WHERE strftime('%Y-%m', OrderDate) = '2023-01'")
        orders = cursor.fetchall()
        conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/order_details/<int:order_id>')
def order_details(order_id):
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Orders.OrderID, Customers.FirstName, Customers.LastName, Customers.Email, OrderItems.ProductID, OrderItems.Quantity 
            FROM Orders 
            JOIN Customers ON Orders.CustomerID = Customers.CustomerID 
            JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID 
            WHERE Orders.OrderID = ?
        ''', (order_id,))
        order_details = cursor.fetchall()
        conn.close()
    return render_template('order_details.html', order_details=order_details)

@app.route('/products_in_order/<int:order_id>')
def products_in_order(order_id):
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Products.ProductName, OrderItems.Quantity 
            FROM OrderItems 
            JOIN Products ON OrderItems.ProductID = Products.ProductID 
            WHERE OrderItems.OrderID = ?
        ''', (order_id,))
        products = cursor.fetchall()
        conn.close()
    return render_template('products.html', products=products)

@app.route('/customer_spending')
def customer_spending():
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) as TotalSpent 
            FROM Customers 
            JOIN Orders ON Customers.CustomerID = Orders.CustomerID 
            JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID 
            JOIN Products ON OrderItems.ProductID = Products.ProductID 
            GROUP BY Customers.CustomerID
        ''')
        spending = cursor.fetchall()
        conn.close()
    return render_template('spending.html', spending=spending)

@app.route('/popular_product')
def popular_product():
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Products.ProductName, SUM(OrderItems.Quantity) as TotalQuantity 
            FROM Products 
            JOIN OrderItems ON Products.ProductID = OrderItems.ProductID 
            GROUP BY Products.ProductID 
            ORDER BY TotalQuantity DESC 
            LIMIT 1
        ''')
        product = cursor.fetchone()
        conn.close()
    return render_template('product.html', product=product)

@app.route('/monthly_sales')
def monthly_sales():
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT strftime('%Y-%m', Orders.OrderDate) as Month, COUNT(*) as TotalOrders, SUM(Products.Price * OrderItems.Quantity) as TotalSales 
            FROM Orders 
            JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID 
            JOIN Products ON OrderItems.ProductID = Products.ProductID 
            WHERE strftime('%Y', Orders.OrderDate) = '2023' 
            GROUP BY Month
        ''')
        sales = cursor.fetchall()
        conn.close()
    return render_template('sales.html', sales=sales)

@app.route('/big_spenders')
def big_spenders():
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) as TotalSpent 
            FROM Customers 
            JOIN Orders ON Customers.CustomerID = Orders.CustomerID 
            JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID 
            JOIN Products ON OrderItems.ProductID = Products.ProductID 
            GROUP BY Customers.CustomerID 
            HAVING TotalSpent > 1000
        ''')
        customers = cursor.fetchall()
        conn.close()
    return render_template('big_spenders.html', customers=customers)

if __name__ == '__main__':
    app.run(debug=True)