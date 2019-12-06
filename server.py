import socket
from time import sleep
class player :
    def __init__(self):
        self.name = ""
        self.nobat = 0
        self.points = 0

    def __str__(self):
        return self.name +",nobat: "+ str(self.nobat)+",points :  "+str(self.points)


def points(squers , edge , ground):
    contain_squers=[]
    point = 0
    print("***************************")
    for squer in squers:
        if edge[0] in squer and edge[1] in squer:
            contain_squers.append(squer)

    for squer in contain_squers:
        if ground[squer[0]][squer[1]]==1 and ground[squer[0]][squer[2]]==1 and ground[squer[1]][squer[3]]==1 and ground[squer[2]][squer[3]]==1:
            point+=1 ;

    print("squers : " , contain_squers)
    print("point : " , point)
    print()
    print("************************")

    return point


def end_game(ground):
    """if all edge is selected"""
    for x in ground:
        for y in x :
            if y == 0 :
                return False

    return True


def make_ground(dimension_x , dimension_y):
    ground=[]
    for x in range(dimension_x * dimension_y ):
        ground.append([])
        for y in range(dimension_x * dimension_y):
            if  y == x + dimension_y  or y == x - dimension_y:
                ground[x].append(0)
            elif  (x % dimension_y != dimension_y - 1) and (x % dimension_y != 0) and (y == x - 1 or y == x + 1):
                ground[x].append(0)
            elif (x % dimension_y == dimension_y - 1)and y==x-1 :
                ground[x].append(0)
            elif (x % dimension_y == 0) and y==x+1:
                ground[x].append(0)
            else:
                ground[x].append(2)

    return ground

def make_list_squere(dimension_x , dimension_y):
    list_squere =[]
    for i in range(dimension_x * dimension_y):
        for j in range(dimension_x * dimension_y):
            for k in range(dimension_x * dimension_y):
                for h in range(dimension_x * dimension_y):
                    if j == i+1 and k == i+dimension_y and h==i+dimension_y+1 and j % dimension_y != 0:
                        list_squere.append([i,j,k,h])

    return list_squere



def gift(point):
    """ if player has gift return true else return false """
    #TODO how to understand a player has gift
    if point == 0:
        return False
    else:
        return True


def re_connect(conn,addr):
    print(conn.fileno())
    print("xxxxxxxxxxx",addr)


HOST = '192.168.43.200'  # Standard loopback interface address (localhost)
PORT = 2000       # Port to listen on (non-privileged ports are > 1023)
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
conn_list=[]
player_list = []

while (True):
    """give dimension of ground"""
    # dimension_x = int (input("input dimension_x :  "))
    # dimension_y = int (input("input dimention_y :  "))
    dimension_x = 8
    dimension_y = 6

    if dimension_x > 10 or dimension_x < 2 or dimension_y>10 or dimension_y < 2 :
        print("dimension must be between 4 and 10 ")
    else:
        print("server is run ")
        ground =make_ground(dimension_x , dimension_y)
        # for index , x in enumerate(ground):
        #     print(index , "   " , x ,"   " , x.count(0))

        # print("________________")
        squers = make_list_squere(dimension_x , dimension_y)
        # for i in squers:
        #     print(i)
        # print("_________________________________")
        # print(len(squers))
        # draw(ground , dimension)
        break

number_player = 2
for i in range(0,number_player):
    """connect 4 client to server"""
    s.listen()
    conn, addr = s.accept()
    conn_list.append((conn, addr))
    conn.sendall((str(i+1)+"\r\n").encode())#nobat
    # conn.sendall(str(dimension_x).encode())
    print(conn_list[i])
    gamer = player()
    gamer.nobat = i+1
    player_list.append(gamer)


for index , item in enumerate(conn_list):
    sleep(0.5)
    print("_______________")
    """give name of client and specify color"""
    conn = item [0]
    addr =item [1]
    conn.sendall("your name ?\r\n".encode())
    name=conn.recv(1024)
    print(name.decode())
    player_list[index].name=name.decode().strip()

for player in player_list:
    """print player"""
    print(player)

index = 0
while True:
    """start game """
    index = index % number_player
    item = conn_list[index]
    if end_game(ground):
        """when game ended send massage to specify winner"""
        win_player = max(player_list, key=lambda player: player.points)
        for item in conn_list:
            print("end_game : ",win_player)

            item[0].sendall(("end Game _ the winner : " + str(win_player)+"\r\n").encode())
        break
    conn=item[0]
    addr=item[1]

    for index2,con in enumerate(conn_list):

        """send to all player Who's the turn """
        if index == index2:
            con[0].sendall("your turn\r\n".encode())
        else:
            print((str(player_list[index].name).encode()))
            con[0].sendall((str(player_list[index].name)+" turn \r\n").encode())

    data = conn.recv(1024) #give edge  forexample 1,2
    print("edge = " , data.decode())
    edge = data.decode().split(",")
    x=int(edge[0])
    y=int(edge[1])

    ground[x][y]=1
    ground[y][x]=1
    print("___squers____:",squers)
    point = points(squers, [x,y], ground)
    player_list[index].points += point
    # draw(ground, dimension_x)
    for player in player_list:
        print(player)
    print("x: ",x , "   y: ",y)
    for con in conn_list:
        """send to all clients what the current turn player send """
        con[0].sendall((str(index) + ":" + data.decode()+"\r\n").encode())

    if not gift(point):
        index += 1

