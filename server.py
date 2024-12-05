import socket
from threading import Thread

CLIENTS = {}

def setup():
    global SERVER
    global IP_ADDRESS
    global PORT

    IP_ADDRESS = '127.0.0.1'
    PORT = 6000

    print("\n\t\t\t\t Welcome to Tambola Game!\n")

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))

    SERVER.listen(10)

    print("\t\t\t\t Server is waiting for incomming connections\n")

    accept_connection()

def accept_connection():
    while True:
        #setup()
        player_socket,addr = SERVER.accept()
        player_name = player_socket.recv(1048).decode().strip()
        print(player_name)
        if(len(CLIENTS.keys())==0):
            CLIENTS[player_name] = {"player_type":'Player 1'}
        else:
            CLIENTS[player_name] = {"player_type":'Player 2'}
        CLIENTS[player_name]["player_socket"] = player_socket
        CLIENTS[player_name]["player_name"]= player_name
        CLIENTS[player_name]["player_addr"] = addr
        CLIENTS[player_name]["turn"]= False

        print(f"Connection established with {player_name}:{addr}")

setup()