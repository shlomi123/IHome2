import _thread
import os
from IHome2.Protocols import Protocols
from IHome2.DBHandler import DBHandler


class Handler():
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

        #  [0] - Protocol code, [1] - username, [2] - file names
        elif messageCode == Protocols.UPLOAD:
            self.handleUpload(parsedCommand[1], parsedCommand[2])

        #  [0] - Protocol code
        elif messageCode == Protocols.SEND_FILES:
            self.handleSendFileNames()

        #  [0] - Protocol code, [1] - username, [2] - file name
        elif messageCode == Protocols.DOWNLOAD:
            self.handleDownload(parsedCommand[1], parsedCommand[2])

        #  [0] - Protocol code, [1] - wifi name, [2] - wifi password
        elif messageCode == Protocols.WIFI_CONFIG:
            self.handleWifiConfig(parsedCommand[1], parsedCommand[2])

        #  [0] - Protocol code
        elif messageCode == Protocols.GET_LOGS:
            self.handleGetLogs()

    def handleRegister(self, username, password, code):
        if code != ('abcd'):  # If code doesn't match
            self.soc.send(Protocols.WRONG_CODE.encode())
            return

        if DBHandler.register(username, password) is True:
            self.soc.send(Protocols.GOOD.encode())
            DBHandler.log(username, Protocols.ACTION_SIGNUP, username + Protocols.CONTENT_SIGNUP)
            self.soc.close()
        else:
            self.soc.send(Protocols.USERNAME_EXISTS.encode())
            self.soc.close()

    def handleLogin(self, username, password):
        if DBHandler.login(username, password) is True:
            self.soc.send(Protocols.GOOD.encode())
            DBHandler.log(username, Protocols.ACTION_LOGIN, username + Protocols.CONTENT_LOGIN)
            self.soc.close()
        else:
            self.soc.send(Protocols.LOGIN_FAILED.encode())
            self.soc.close()

    def handleUpload(self, username, fileNames):
        counter = 1
        parsedFileNames = fileNames.split('&&')
        print(parsedFileNames)
        self.soc.send(Protocols.GOOD.encode())  # approve that file names were received

        # start receiving files from client
        self.soc.settimeout(5)
        for fileName in parsedFileNames:
            file = open("files\\" + fileName, 'wb')
            print("in loop " + str(counter))
            counter = counter + 1
            DBHandler.log(username, Protocols.ACTION_FILE_UPLOAD, fileName)

            while True:
                try:
                    data = self.soc.recv(1024)
                    print(data)
                    code = data[-3:]
                    print(code)
                    if code == b'200':
                        data = data[0:-3]
                        file.write(data)
                        print("end")
                        self.soc.send(Protocols.GOOD.encode())
                        break

                    file.write(data)
                except Exception as e:
                    print(e)
                    break

            file.close()

        print ("out of loops")
        self.soc.send(Protocols.GOOD.encode())  # approve that files were received"""
        self.soc.close()

    def handleSendFileNames(self):
        names = Protocols.GOOD + "&&"
        for i in os.listdir("files\\"):
            names = names + i + "&&"
        names = names[0:-2]
        print(names)
        self.soc.send(names.encode())
        self.soc.close()

    def handleDownload(self, username, fileName):
        self.soc.send(Protocols.GOOD.encode())
        print(fileName)
        ans = self.soc.recv(1024).decode('UTF-8')
        # TODO finish sending file to client
        try:
            if ans == Protocols.GOOD:
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
            DBHandler.log(username, Protocols.ACTION_FILE_DOWNLOAD, fileName)
            self.soc.close()
        except Exception as e:
            file.close()
            self.soc.close()
            print(e)

    def handleWifiConfig(self, name, password):
        # TODO connect to wifi
        self.soc.close()
        return

    def handleGetLogs(self):
        message = DBHandler.getLogs()

        self.soc.send(message.encode())
        self.soc.close()
