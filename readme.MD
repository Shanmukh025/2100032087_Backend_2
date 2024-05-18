# Safertek Backend Task

This is the README file for the Safertek Backend Developer Task by *2100032087cseh@gmail.com*.

## Queries Used

1. List all customers:

    ```sql
    SELECT * FROM Customers
    ```

2. Find all orders placed in January 2023:

    ```sql
    SELECT * FROM Orders WHERE strftime('%Y-%m', OrderDate) = '2023-01'
    ```

3. Get the details of each order, including the customer name and email:

    ```sql
    SELECT Orders.OrderID, Customers.FirstName, Customers.LastName, Customers.Email, OrderItems.ProductID, OrderItems.Quantity
    FROM Orders
    JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    WHERE Orders.OrderID = ?
    ```

4. List the products purchased in a specific order (e.g., OrderID = 1):

    ```sql
    SELECT Products.ProductName, OrderItems.Quantity
    FROM OrderItems
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    WHERE OrderItems.OrderID = ?
    ```

5. Calculate the total amount spent by each customer:

    ```sql
    SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) as TotalSpent
    FROM Customers
    JOIN Orders ON Customers.CustomerID = Orders.CustomerID
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    GROUP BY Customers.CustomerID
    ```

6. Find the most popular product (the one that has been ordered the most):

    ```sql
    SELECT Products.ProductName, SUM(OrderItems.Quantity) as TotalQuantity
    FROM Products
    JOIN OrderItems ON Products.ProductID = OrderItems.ProductID
    GROUP BY Products.ProductID
    ORDER BY TotalQuantity DESC
    LIMIT 1
    ```

7. Get the total number of orders and the total sales amount for each month in 2023:

    ```sql
    SELECT strftime('%Y-%m', Orders.OrderDate) as Month, COUNT(*) as TotalOrders, SUM(Products.Price * OrderItems.Quantity) as TotalSales
    FROM Orders
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    WHERE strftime('%Y', Orders.OrderDate) = '2023'
    GROUP BY Month
    ```

8. Find customers who have spent more than $1000:
    ```sql
    SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) as TotalSpent
    FROM Customers
    JOIN Orders ON Customers.CustomerID = Orders.CustomerID
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    GROUP BY Customers.CustomerID
    HAVING TotalSpent > 1000
    ```
