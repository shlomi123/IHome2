import socket
from IHome2.Handler import Handler


def main():
    serv_soc = socket.socket()
    serv_soc.bind(('0.0.0.0', 1618))
    print('Server started...')
    serv_soc.listen(1)
    
    while True:
        try:
            print('Listening...')
            client_soc, client_address = serv_soc.accept()
            print('Received connection from client: ' + str(client_address))

            command = client_soc.recv(1024).decode('UTF-8')
            handler = Handler(client_soc)
            handler.parseCommandAndHandle(command)

            client_soc.close()
        except Exception as e:
            print(e)
            break
        
    serv_soc.close()


if __name__=='__main__':
    main()
