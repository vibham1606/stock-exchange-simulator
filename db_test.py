import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="stock_exchange",
        user="postgres",
        password="Password@16"
    )

    print("Connected Successfully!")

    conn.close()

except Exception as e:
    print("Error:", e)