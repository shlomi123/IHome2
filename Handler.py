import sqlite3
from IHome2.Protocols import Protocols


class Handler:
    soc = 0

    def __init__(self, client_soc):
        self.soc = client_soc

    def parseCommandAndHandle(self, command):
        messageCode = command[0:3]
        parsedCommand = command.split('@@')

        #  [0] - Protocol code, [1] - Username, [2] - Password
        if messageCode == Protocols.LOG_IN:  ## If Login
            self.handleLogin(parsedCommand[1], parsedCommand[2])

        #  [0] - Protocol code, [1] - Username, [2] - Password, [3] - code
        elif messageCode == Protocols.REGISTER:  ## If Register
            self.handleRegister(parsedCommand[1], parsedCommand[2], parsedCommand[3])

        #  [0] - Protocol code, [1] - file names
        elif messageCode == Protocols.UPLOAD:  ## If upload files
            self.handleUpload(parsedCommand[1])

    def handleRegister(self, username, password, code):
        if code != ('abcd'):  # If code doesn't match
            self.soc.send(Protocols.WRONG_CODE.encode())
            return

        con = sqlite3.connect('Database.db')  # Open the database
        c = con.cursor()

        # Check if user exists
        c.execute("SELECT count(*) FROM users WHERE username=?", (username,))
        count = c.fetchone()[0]

        if count > 0:  # If the username is taken
            self.soc.send(Protocols.USERNAME_EXISTS.encode())
            print('Username is taken')
            return

        # Insert user to database
        c.execute("INSERT INTO users VALUES (? ,?, ?)", (None, username, password))
        con.commit()

        print('INSERTED')
        self.soc.send(Protocols.GOOD.encode())
        return

    def handleLogin(self, username, password):
        con = sqlite3.connect('Database.db')  ## Open the database
        c = con.cursor()

        ## Check if username and password match
        c.execute("SELECT count(*) FROM users WHERE username=? AND password=?", (username, password))
        count = c.fetchone()[0]

        if count > 0:  ## If the values match
            print('Login successful')
            self.soc.send(Protocols.GOOD.encode())
            return

        print('Wrong username or password')
        self.soc.send(Protocols.LOGIN_FAILED.encode())
        return

    def handleUpload(self, fileNames):
        parsedFileNames = fileNames.split('&&')
        print (parsedFileNames)
        self.soc.send(Protocols.GOOD.encode())  # approve that file names were received

        data = self.soc.recv(1024)
        print(data)
        """for fileName in parsedFileNames:
            #file = open(fileName, 'wb')
            print ("in first loop")
            while True:
               data = self.soc.recv(1024)
               print(data)
               if not data: break
               #file.write(data)

            #file.close()

        self.soc.send(Protocols.GOOD.encode())  # approve that files were received"""
        return