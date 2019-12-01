import socket

def make_ground(dimension):
    ground = []
    for x in range(dimension ** 2):
        ground.append([])
        for y in range(dimension ** 2):
            if y == x + dimension or y == x - dimension:
                ground[x].append(0)
            elif (x % dimension != dimension - 1) and (x % dimension != 0) and (y == x - 1 or y == x + 1):
                ground[x].append(0)
            elif (x % dimension == dimension - 1) and y == x - 1:
                ground[x].append(0)
            elif (x % dimension == 0) and y == x + 1:
                ground[x].append(0)
            else:
                ground[x].append(2)

    return ground



HOST = '192.168.43.200'  # The server's hostname or IP address
PORT = 65432    # The port used by the server
print(PORT)
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = s.recv(1024)
print("nobat : " , data.decode())
# data=s.recv(1024)
# print("dimension : " , data.decode())
# dimension=int(data.decode())
name = input("your name :  ")
s.sendall(name.encode())
# ground = make_ground(dimension)
# print(ground)

while True:
    data=s.recv(1024)
    print("recive:" , data.decode())
    if data.decode() == "your turn" :
        data = input()
        s.sendall(data.encode())

    # s.sendall(b'Hello, world')
    data = s.recv(1024)
    print("recive:" , data.decode())

