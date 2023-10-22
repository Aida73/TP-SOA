import logging
logging.basicConfig(level=logging.DEBUG)
import sqlite3

def create_solv_db():
    conn = sqlite3.connect('tp1Db.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        client_id INTEGER PRIMARY KEY,
        prenom TEXT,
        nom TEXT,
        email TEXT,
        telephone INTEGER,
        adresse TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pret (
        pret_id INTEGER PRIMARY KEY,
        client_id INTEGER,
        montant REAL,
        date DATE,
        FOREIGN KEY (client_id) REFERENCES Clients(client_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Demande (
        demande_id INTEGER PRIMARY KEY,
        client_id INTEGER,
        request_text TEXT,
        request_date DATE,
        FOREIGN KEY (client_id) REFERENCES Clients(client_id)
    )
    ''')
    conn.commit()





# # Insert data into the Clients table
# cursor.execute("INSERT INTO Clients (first_name, last_name, email) VALUES (?, ?, ?)",
#                ("John", "Doe", "john.doe@example.com"))
# cursor.execute("INSERT INTO Clients (first_name, last_name, email) VALUES (?, ?, ?)",
#                ("Alice", "Smith", "alice.smith@example.com"))

# # Insert data into the Pret (Loan) table
# cursor.execute("INSERT INTO Pret (client_id, amount, date_issued) VALUES (?, ?, ?)",
#                (1, 10000.0, "2023-03-01"))
# cursor.execute("INSERT INTO Pret (client_id, amount, date_issued) VALUES (?, ?, ?)",
#                (1, 5000.0, "2023-05-15"))
# cursor.execute("INSERT INTO Pret (client_id, amount, date_issued) VALUES (?, ?, ?)",
#                (2, 7500.0, "2023-04-10"))

# # Insert data into the Demande (Request) table
# cursor.execute("INSERT INTO Demande (client_id, request_text, request_date) VALUES (?, ?, ?)",
#                (1, "I need a loan for a car.", "2023-06-20"))
# cursor.execute("INSERT INTO Demande (client_id, request_text, request_date) VALUES (?, ?, ?)",
#                (2, "Looking for a home loan.", "2023-07-05"))

#conn.commit()
    

