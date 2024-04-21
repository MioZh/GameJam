import sqlite3

# Connect to the database (or create it if it doesn't exist)
db = sqlite3.connect('players.db')

# Create a cursor object to execute SQL commands
cur = db.cursor()

# Create the users table
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        record INTEGER DEFAULT 0,
        games INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS quetions (
        id INTEGER PRIMARY KEY,
        quetion TEXT NOT NULL,
        submits TEXT NOT NULL
    )
''')


def check_quetions():
    try:
        # Connect to the database
        db = sqlite3.connect('players.db')
        cur = db.cursor()

        # Check if the username and password combination exists
        cur.execute('''SELECT * FROM quetions''')
        user = cur.fetchall()  # Fetch one row

        # Close the database connection
        db.close()

        # If user is not None, it means the combination exists
        if user:
            return user
        else:
            return "No users"
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False


#print(check_quetions())

def quet(quetion, submit):
    try:
        # Connect to the database
        db = sqlite3.connect('players.db')
        cur = db.cursor()
        # Insert the new user into the database
        cur.execute('''INSERT INTO quetions (quetion, submits) VALUES (?, ?)''', (quetion, submit))
        db.commit()  # Commit the transaction
        db.close()
        return True
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False


#print(quet("What kind of light has the longest wavelength?", "infrared"))


def get_quetion(id):
    try:
        # Connect to the database
        db = sqlite3.connect('players.db')
        cur = db.cursor()
        # Insert the new user into the database
        cur.execute(f'''SELECT * FROM quetions WHERE id={id}''')
        quation = cur.fetchone()
        db.close()
        return quation
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

#print(type(get_quetion(20)))

def register_user(username, password):
    try:
        # Connect to the database
        db = sqlite3.connect('players.db')
        cur = db.cursor()

        # Check if the username already exists
        cur.execute('''SELECT * FROM users WHERE name=?''', (username,))
        user = cur.fetchone()

        if not user:
            # Insert the new user into the database
            cur.execute('''INSERT INTO users (name, password) VALUES (?, ?)''', (username, password))
            db.commit()  # Commit the transaction
            db.close()
            return True
        else:
            db.close()
            return False
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False



#print(register_user("Azamat", "asdf55"))

def check_credentials(username, password):
    try:
        # Connect to the database
        db = sqlite3.connect('players.db')
        cur = db.cursor()

        # Check if the username and password combination exists
        cur.execute('''SELECT * FROM users WHERE name=? AND password=?''', (username, password))
        user = cur.fetchone()  # Fetch one row

        # Close the database connection
        db.close()

        # If user is not None, it means the combination exists
        if user:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

#print(check_credentials("Azamat", "asd55"))

def not_win_user(username):
    try:
        # Connect to the database
        db = sqlite3.connect('players.db')
        cur = db.cursor()

        # Check if the username already exists
        cur.execute('''SELECT * FROM users WHERE name=?''', (username,))
        user = cur.fetchone()

        if user:
            print(username)
            # Insert the new user into the database
            cur.execute('''
                        UPDATE users
                        SET games = games + 1
                        WHERE name = ?
                        ''', (username,))
            db.commit()  # Commit the transaction
            db.close()
            return True
        else:
            db.close()
            return False
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False


def record_user(username, record):
    try:
        # Connect to the database
        db = sqlite3.connect('players.db')
        cur = db.cursor()

        # Check if the username already exists
        cur.execute('''SELECT * FROM users WHERE name=?''', (username,))
        user = cur.fetchone()

        if user:
            print(record)
            # Insert the new user into the database
            cur.execute('''
                        UPDATE users
                        SET record = ?, wins = wins + 1, games = games + 1
                        WHERE name = ?
                        ''', (record, username))
            db.commit()  # Commit the transaction
            db.close()
            return True
        else:
            db.close()
            return False
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False


def check_users():
    try:
        # Connect to the database
        db = sqlite3.connect('players.db')
        cur = db.cursor()

        # Check if the username and password combination exists
        cur.execute('''SELECT * FROM users''')
        user = cur.fetchone()  # Fetch one row

        # Close the database connection
        db.close()

        # If user is not None, it means the combination exists
        if user:
            return user
        else:
            return "No users"
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

#print(check_users())

# Commit the changes and close the connection
db.commit()
db.close()
