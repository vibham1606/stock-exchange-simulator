import psycopg2
import os

conn = psycopg2.connect(
    host="localhost",
    database="stock_exchange",
    user="postgres",
    password="Password@16"
)

cursor = conn.cursor()

while True:

    print("\n===== STOCK EXCHANGE =====")
    print("1. View Users")
    print("2. View Orders")
    print("3. View Trades")
    print("4. View Portfolio")
    print("5. Create User")
    print("6. Place Order")
    print("7. Run Matching Engine")
    print("8. View Order Book")
    print("9. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":

        cursor.execute("SELECT * FROM Users")

        users = cursor.fetchall()

        print("\nUSERS\n")

        for user in users:
            print(user)

    elif choice == "2":

        cursor.execute("SELECT * FROM Orders")

        orders = cursor.fetchall()

        print("\nORDERS\n")

        for order in orders:
            print(order)

    elif choice == "3":

        cursor.execute("SELECT * FROM Trades")

        trades = cursor.fetchall()

        print("\nTRADES\n")

        for trade in trades:
            print(trade)

    elif choice == "4":

        user_id = int(input("Enter User ID: "))

        cursor.execute("""
        SELECT
        Users.name,
        Stocks.symbol,
        Portfolio.quantity
        FROM Portfolio
        JOIN Users
        ON Portfolio.user_id = Users.user_id
        JOIN Stocks
        ON Portfolio.stock_id = Stocks.stock_id
        WHERE Users.user_id = %s
        """,
        (user_id,)
        )

        portfolio = cursor.fetchall()

        print("\nPORTFOLIO\n")

        for p in portfolio:
            print(p)

    elif choice == "5":

        user_id = int(input("User ID: "))
        name = input("Name: ")
        balance = int(input("Balance: "))

        cursor.execute(
        """
        INSERT INTO Users
        (user_id,name,balance,shares)
        VALUES(%s,%s,%s,%s)
        """,
        (
            user_id,
            name,
            balance,
            0
        )
    )

        conn.commit()

        print("User Added Successfully!")

    elif choice == "6":

        order_id = int(input("Order ID: "))
        user_id = int(input("User ID: "))

        order_type = input("BUY or SELL: ").upper()

        price = int(input("Price: "))
        quantity = int(input("Quantity: "))

        stock_id = int(input("Stock ID: "))
        
        if order_type == "BUY":

            cursor.execute("""
            SELECT balance
            FROM Users
            WHERE user_id = %s
            """,
            (user_id,))

            balance = cursor.fetchone()[0]

            required_amount = price * quantity

        if balance < required_amount:

            print("\nOrder Rejected!")
            print("Insufficient Balance")

            continue

        if order_type == "SELL":

            cursor.execute("""
            SELECT quantity
            FROM Portfolio
            WHERE user_id = %s
            AND stock_id = %s
            """,
            (
                user_id,
                stock_id
            ))

            result = cursor.fetchone()

            if result is None:

                print("\nOrder Rejected!")
                print("You don't own this stock")

                continue

            owned_qty = result[0]

            if quantity > owned_qty:

                print("\nOrder Rejected!")
                print("Not enough shares")

                continue

        cursor.execute(
        """
        INSERT INTO Orders
        (order_id,user_id,order_type,price,quantity,stock_id)
        VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (
            order_id,
            user_id,
            order_type,
            price,
            quantity,
            stock_id
        )
    )

        conn.commit()

        print("Order Added Successfully!")
    
    elif choice == "7":

        os.system("python matching_engine.py")

    
    elif choice == "8":

        print("\nBUY ORDERS\n")

        cursor.execute("""
        SELECT
        Orders.order_id,
        Users.name,
        Stocks.symbol,
        Orders.price,
        Orders.quantity
        FROM Orders
        JOIN Users
        ON Orders.user_id = Users.user_id
        JOIN Stocks
        ON Orders.stock_id = Stocks.stock_id
        WHERE Orders.order_type = 'BUY'
        ORDER BY Orders.price DESC
        """)

        buy_orders = cursor.fetchall()

        for order in buy_orders:
            print(order)

        print("\nSELL ORDERS\n")

        cursor.execute("""
        SELECT
        Orders.order_id,
        Users.name,
        Stocks.symbol,
        Orders.price,
        Orders.quantity
    FROM Orders
    JOIN Users
    ON Orders.user_id = Users.user_id
    JOIN Stocks
    ON Orders.stock_id = Stocks.stock_id
    WHERE Orders.order_type = 'SELL'
    ORDER BY Orders.price ASC
    """)

        sell_orders = cursor.fetchall()

        for order in sell_orders:
            print(order)

    elif choice=="9":
        break

cursor.close()
conn.close()
