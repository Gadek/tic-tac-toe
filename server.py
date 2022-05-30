import socket
from _thread import *
from game import Game
import pickle

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    print(pickle.dumps(p))
    conn.send(pickle.dumps(p))

    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data[:4]=="nick":
                        game.set_nickname(p,data[4:])
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    print("Conn:", conn)
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    print(gameId)
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))
