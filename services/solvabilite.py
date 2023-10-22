import sqlite3
from utils import createDatabase
db = createDatabase.create_solv_db()
# Connect to the database
conn = sqlite3.connect('tp1Db.db')

# Create a cursor
cursor = conn.cursor()

# Get a list of tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the list of tables
for table in tables:
    print("Table:", table[0])

# Close the connection
conn.close()
