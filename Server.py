import socket
import os
import sqlite3

## Parses the command we got from client and sends it to the handeling function
def parseCommandAndHandle(command, client_soc):
   isOk = False      ## Will return true if process finished with success
   messageCode = command[0:3]  
           
     
   parsedCommand = command.split('@@')
   
   ##  [0] - Protocol code, [1] - Username, [2] - Password, [3] - code 
   if messageCode == '101':     ## If Login
       isOk = handleLogin(parsedCommand[1], parsedCommand[2])
   elif messageCode == '102':     ## If Register
       isOk = handleRegister(parsedCommand[1], parsedCommand[2], parsedCommand[3])
   ##  [0] - Protocol code, [1] - file names
   elif messageCode == '103':     ## If upload files
        isOk = handleUpload(client_soc, parsedCommand[1])
        return isOk
   
        
   return isOk
        
def handleRegister(username, password, code):
    if (code != 'abcd'):       ## If code doesn't match
        return False
    
    con = sqlite3.connect('Database.db')   ## Open the database
    c = con.cursor()
    
    ## Check if user exists
    c.execute("SELECT count(*) FROM users WHERE username=?", (username,)) 
    
    count = c.fetchone()[0]
    
    if count > 0:  ## If the username is taken
        print('Username is taken')
        return False
    
    ## Insert user to database
    c.execute("INSERT INTO users VALUES (? ,?, ?)", (None ,username, password))
    con.commit()
    
    print('INSERTED')
    
    return True

def handleLogin(username, password):
    con = sqlite3.connect('Database.db')   ## Open the database
    c = con.cursor()
    
    ## Check if username and password match
    c.execute("SELECT count(*) FROM users WHERE username=? AND password=?", (username,password)) 

    count = c.fetchone()[0]
    
    if count > 0: ## If the values match
        print('Login successful')
        return True
    
    print('Wrong username or password')
    return False

def handleUpload(client_soc, fileNames):
    parsedFileNames = fileNames.split('&&')
    print(parsedFileNames)
    returnCode = '200'
    
    for fileName in parsedFileNames:
        file = open(fileName, 'wb')
        while True:
           data = client_soc.recv(1024)
           print(data)
           if not data: break
           file.write(data)    
           print('Writing file')           
           
        client_soc.send(returnCode.encode())   
        file.close()
       
    return True
    
def main():
    serv_soc = socket.socket()
    serv_soc.bind(('0.0.0.0', 1618))
    print('Server started. Listening...')
    serv_soc.listen(1)
    
    while True:
        client_soc, client_address = serv_soc.accept()
        print('Received connection from client')
        
        command = client_soc.recv(1024).decode('UTF-8')
        print(command)
        isOk = parseCommandAndHandle(command, client_soc)
        
        ## Return isOK to app
        
    serv_soc.close()
    
if __name__=='__main__':
    main()
    