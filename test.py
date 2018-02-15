import socket
GOOD = "200"
BLAA = "106"
# 105@@filename

# Create a TCP/IP socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 1618)
soc.connect(server_address)

print("connected to server")

code = "106"

soc.send(code.encode())

ret = soc.recv(1024)

print(ret.decode())
