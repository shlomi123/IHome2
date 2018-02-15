import sqlite3
import datetime


class DBHandler:
    @staticmethod
    def log(username, action, content):
        conn = sqlite3.connect("log.db")
        date = datetime.datetime.now().strftime("%d-%m-%y")
        conn.execute("INSERT INTO LOG VALUES(?,?,?,?,?)", (None, username, date, action, content))
        conn.commit()

    @staticmethod
    def register(username, password):
        con = sqlite3.connect('Database.db')  # Open the database
        c = con.cursor()

        # Check if user exists
        c.execute("SELECT count(*) FROM users WHERE username=?", (username,))
        count = c.fetchone()[0]

        if count > 0:  # If the username is taken
            print('Username is taken')
            return False

        # Insert user to database
        c.execute("INSERT INTO users VALUES (? ,?, ?)", (None, username, password))
        con.commit()
        print('Register fail')
        return True

    @staticmethod
    def login(username, password):
        con = sqlite3.connect('Database.db')  # Open the database
        c = con.cursor()

        # Check if username and password match
        c.execute("SELECT count(*) FROM users WHERE username=? AND password=?", (username, password))
        count = c.fetchone()[0]

        if count > 0:  # If the values match
            print('Login successful')
            return True
        else:
            print('Login failed')

    @staticmethod
    def getLogs():
        conn = sqlite3.connect("log.db")
        cursor = conn.execute("SELECT USERNAME, DATE, ACTION, CONTENT FROM LOG")

        message = ""

        for row in cursor:
            message = message + row[0] + "@@" + row[1] + "@@" + row[2] + "@@" + row[3] + "&&"

        return message[0:-2]
