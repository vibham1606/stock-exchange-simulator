import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="stock_exchange",
        user="postgres",
        password="Password@16"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users")

    rows = cursor.fetchall()

    print("\nUSERS TABLE\n")

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)