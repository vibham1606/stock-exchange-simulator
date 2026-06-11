import psycopg2

def run_matching():
    conn = psycopg2.connect(
    host="localhost",
    database="stock_exchange",
    user="postgres",
    password="Password@16"
)

    cursor = conn.cursor()

    try:

        cursor.execute("""
        SELECT *
        FROM Orders
        WHERE order_type='BUY'
        ORDER BY price DESC
        """)


        buy_orders = cursor.fetchall()

        cursor.execute("""
        SELECT *
        FROM Orders
        WHERE order_type='SELL'
        ORDER BY price ASC
        """)

        sell_orders = cursor.fetchall()

        i = 0
        j = 0

        while i < len(buy_orders) and j < len(sell_orders):

            buy = list(buy_orders[i])
            sell = list(sell_orders[j])

            buy_order_id = buy[0]
            buyer_id = buy[1]
            buy_price = buy[3]
            buy_qty = buy[4]
            buy_stock = buy[5]

            sell_order_id = sell[0]
            seller_id = sell[1]
            sell_price = sell[3]
            sell_qty = sell[4]
            sell_stock = sell[5]

            print("\nChecking:")
            print("Buy :", buy_order_id, "Stock:", buy_stock, "Price:", buy_price)
            print("Sell:", sell_order_id, "Stock:", sell_stock, "Price:", sell_price)

            if buy_stock == sell_stock and buy_price >= sell_price:

                traded_qty = min(buy_qty, sell_qty)

                trade_price = sell_price

                trade_value = traded_qty * trade_price

                print("\nTRADE EXECUTED")
                print("Buyer:", buyer_id)
                print("Seller:", seller_id)
                print("Price:", trade_price)
                print("Quantity:", traded_qty)

                # Insert Trade
                cursor.execute("""
                INSERT INTO Trades
                (buyer_id,seller_id,trade_price,quantity)
                VALUES(%s,%s,%s,%s)
                """,
                (
                    buyer_id,
                    seller_id,
                    trade_price,
                    traded_qty
                ))

                # Update Buyer
                cursor.execute("""
                UPDATE Users
                SET balance = balance - %s
                WHERE user_id = %s
                """,
                (
                    trade_value,
                    
                    buyer_id
                ))

            # Update Buyer Portfolio

                cursor.execute("""
                INSERT INTO Portfolio
                (user_id, stock_id, quantity)

                VALUES(%s,%s,%s)

                ON CONFLICT (user_id, stock_id)

                DO UPDATE SET
                quantity = Portfolio.quantity + EXCLUDED.quantity
                    """,
                    (
                    buyer_id,
                    buy_stock,
                    traded_qty
                    ))

                # Update Seller
                cursor.execute("""
                UPDATE Users
                SET balance = balance + %s
                WHERE user_id = %s
                """,
                (
                    trade_value,
                    
                    seller_id
                ))

                # Update Seller Portfolio

                cursor.execute("""
                UPDATE Portfolio
                SET quantity = quantity - %s
                WHERE user_id = %s
                AND stock_id = %s
                """,
                (
                    traded_qty,
                    seller_id,
                    buy_stock
                ))

                buy_qty -= traded_qty
                sell_qty -= traded_qty

                cursor.execute("""
                DELETE FROM Portfolio
                WHERE quantity <= 0
                """)

                # Update/Delete Buy Order
                if buy_qty == 0:

                    cursor.execute("""
                    DELETE FROM Orders
                    WHERE order_id = %s
                    """,
                    (buy_order_id,))

                    i += 1

                else:

                    cursor.execute("""
                    UPDATE Orders
                    SET quantity = %s
                    WHERE order_id = %s
                    """,
                    (
                        buy_qty,
                        buy_order_id
                    ))

                    i += 1

                # Update/Delete Sell Order
                if sell_qty == 0:

                    cursor.execute("""
                    DELETE FROM Orders
                    WHERE order_id = %s
                    """,
                    (sell_order_id,))

                    j += 1

                else:

                    cursor.execute("""
                    UPDATE Orders
                    SET quantity = %s
                    WHERE order_id = %s
                    """,
                    (
                        sell_qty,
                        sell_order_id
                    ))

                    j += 1

            else:

                if buy_stock != sell_stock:
                    j += 1
                else:
                    break

        conn.commit()

        print("\nMatching Complete!")

    except Exception as e:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_matching()