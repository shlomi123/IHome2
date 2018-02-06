import sqlite3
from IHome2.Protocols import Protocols
import os
import socket


class Handler:
    soc = 0

    def __init__(self, client_soc):
        self.soc = client_soc

    def parseCommandAndHandle(self, command):
        messageCode = command[0:3]
        parsedCommand = command.split('@@')

        #  [0] - Protocol code, [1] - Username, [2] - Password
        if messageCode == Protocols.LOG_IN:
            self.handleLogin(parsedCommand[1], parsedCommand[2])

        #  [0] - Protocol code, [1] - Username, [2] - Password, [3] - code
        elif messageCode == Protocols.REGISTER:
            self.handleRegister(parsedCommand[1], parsedCommand[2], parsedCommand[3])

        #  [0] - Protocol code, [1] - file names
        elif messageCode == Protocols.UPLOAD:
            self.handleUpload(parsedCommand[1])

        #  [0] - Protocol code
        elif messageCode == Protocols.SEND_FILES:
            self.handleSendFileNames()

        #  [0] - Protocol code, [1] - file name
        elif messageCode == Protocols.DOWNLOAD:
            self.handleDownload(parsedCommand[1])

        #  [0] - Protocol code, [1] - wifi name, [2] - wifi password
        elif messageCode == Protocols.WIFI_CONFIG:
            self.handleWifiConfig()

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
        counter = 1
        parsedFileNames = fileNames.split('&&')
        print (parsedFileNames)
        self.soc.send(Protocols.GOOD.encode())  # approve that file names were received

        # start receiving files from client
        self.soc.settimeout(5)
        for fileName in parsedFileNames:
            file = open("files\\" + fileName, 'wb')
            print ("in loop " + str(counter))
            counter = counter + 1

            while True:
                try:
                    data = self.soc.recv(1024)
                    print (data)
                    code = data[-3:]
                    print (code)
                    if code == b'200':
                        data = data[0:-3]
                        file.write(data)
                        print ("end")
                        self.soc.send(Protocols.GOOD.encode())
                        break

                    file.write(data)
                except Exception as e:
                    print (e)
                    break

            file.close()

        print ("out of loops")
        self.soc.send(Protocols.GOOD.encode())  # approve that files were received"""
        return

    def handleSendFileNames(self):
        names = Protocols.GOOD + "&&"
        for i in os.listdir("files\\"):
            names = names + i + "&&"
        names = names[0:-2]
        print (names)
        self.soc.send(names.encode())

        return

    def handleDownload(self, fileName):
        self.soc.send(Protocols.GOOD.encode())
        print(fileName)
        ans = self.soc.recv(1024).decode('UTF-8')
        # TODO finish sending file to client
        try:
            if ans == "200":
                print(ans)
                file = open("files\\" + fileName, 'rb')

                bytes = file.read(1024)
                while (bytes):
                    self.soc.send(bytes)
                    bytes = file.read(1024)
                    print(bytes)
                file.close()
            else:
                print("client didn't confirm")
        except Exception as e:
            file.close()
            print (e)

        return

    def handleWifiConfig(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        self.soc.send(str(ip).encode())
        return
