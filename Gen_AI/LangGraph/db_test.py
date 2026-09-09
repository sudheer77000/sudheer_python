import sqlite3

# Connect to a database (creates the file if it doesn't exist)
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# Create a table
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
)

# Insert data
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
conn.commit()

# Query data
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

# Close the connection
conn.close()