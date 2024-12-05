import socket
from threading import Thread
from tkinter import *
import random
from PIL import ImageTk,Image
import platform

ticket_grid = []
current_no_list = []
displayed_number_list = []

def ask_name():
    global player_name
    global name_entry
    global canvas1
    global nameWindow
    global screen_width
    global screen_height

    nameWindow = Tk()
    nameWindow.title("Tambola")
    nameWindow.geometry('800x600')

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()
    print(screen_width,screen_height)

    bg = ImageTk.PhotoImage(file="assets/background.png")

    canvas1 = Canvas(nameWindow,width=500,height=500)
    canvas1.pack(fill="both",expand=True)
    canvas1.create_image(0,0,image=bg,anchor='nw')
    canvas1.create_text(screen_width/4.5,screen_height/8,text='Enter your name :', font=('Chalkboard SE',60),fill="black")

    name_entry = Entry(nameWindow,justify="center",bd=5,bg='white',font=('Chalkboard SE',30),width=15)
    name_entry.place(x=screen_width/7,y=screen_height/5.5)

    button = Button(nameWindow,text="Save",font=("Chalkboard SE",30),width=11,command=save_name,height=2,bg='#80deea',bd=3)
    button.place(x=screen_width/6,y=screen_height/4)

    nameWindow.resizable(True,True)
    nameWindow.mainloop()

def gameWindow():
    global game_window
    global canvas2
    global screen_height
    global screen_width
    global player_name
    global flash_label

    game_window = Tk()
    game_window.title("Tambola")
    game_window.geometry(f"800x600")

    bg = ImageTk.PhotoImage(file="assets/background.png")

    canvas2 = Canvas(game_window,width=500,height=500)
    canvas2.pack(fill="both",expand=True)
    canvas2.create_image(0,0,image=bg,anchor='nw')
    canvas2.create_text(screen_width/4,screen_height/10,text='Tambola Family Fun', font=('Chalkboard SE',40),fill="black")

    flash_label = canvas2.create_text(400,screen_height/2,text='Waiting for the other to join...', font=('Chalkboard SE',40),fill="black")

    createTicket()
    place_number()

    game_window.resizable(False,False)
    game_window.mainloop()

def createTicket():
    global game_window
    global ticket_grid

    border = Label(game_window,relief="ridge",width=65,height=16,borderwidth=5,border=5)
    border.place(x=95,y=119)

    xPos = 105
    yPos = 130

    for row in range(0,3):
        rowList = []

        for col in range(0,9):
            if(platform.system()=="Darwin"):
                button = Button(game_window,bg="lightyellow",highlightbackground="lightyellow",activebackground="lightgreen",font=("Chalkboard SE",18),pady=23,padx=-22,borderwidth=3)
                button.place(x=xPos,y=yPos)
            else:
                button = Tk.Button(game_window,bg="lightyellow",font=("Chalkboard SE",30),borderwidth=5,width=3,height=2)
                button.place(x=xPos,y=yPos)
            rowList.append(button)
            xPos += 64

        ticket_grid.append(rowList)
        xPos = 105
        yPos += 82

def place_number():
    global ticket_grid
    global current_no_list

    for i in range(0,3):
        random_col_list = []

        counter=0

        while counter<5:
            random_no = random.randint(0,8)
            if (random_no not in random_col_list):
                random_col_list.append(random_no)

            number_container = {
            "0": [1,2,3,4,5,6,7,8,9],
            "1": [10,11,12,13,14,15,16,17,18,19],
            "2": [20,21,22,23,24,25,26,27,28,29],
            "3": [30,31,32,33,34,35,36,37,38,39],
            "4": [40,41,42,43,44,45,46,47,48,49],
            "5": [50,51,52,53,54,55,56,57,58,59],
            "6": [60,61,62,63,64,65,66,67,68,69],
            "7": [70,71,72,73,74,75,76,77,78,79],
            "8": [80,81,82,83,84,85,86,87,88,89]
            }
            while counter<len(random_col_list):
                colNum = random_col_list[counter]
                numbersListByIndex = number_container[str(colNum)]
                random_no = random.choice(numbersListByIndex)

                if (random_no not in current_no_list):
                    number_box = ticket_grid[i][colNum]
                    number_box.configure(text=random_no,fg="black")
                    current_no_list.append(random_no)

                    counter+=1

        print(random_col_list)

def rcv_msg():
    global SERVER
    global flash_label
    global canvas2
    global game_over
    global displayed_number_list

    numbers = []
    for i in range(0,90):
        numbers.append(str(i+1))
    
    while True:
        chunk = SERVER.recv(2048).decode()
        print(chunk)
        if (chunk in numbers and chunk in flash_label and chunk not in game_over):
            flash_label.append(int(chunk))
            canvas2.itemconfigure(flash_label,text=chunk,font=("Chalkboard SE",60))
        elif('wins the game' in chunk):
            game_over = True
            canvas2.itemconfigure(flash_label,text=chunk,font=("Chalkboard SE",40))


def save_name():
    global SERVER
    global player_name
    global nameWindow
    global name_entry

    player_name = name_entry.get()
    name_entry.delete(0,END)
    nameWindow.destroy()

    SERVER.send(player_name.encode())

    gameWindow()

def setup():
    global SERVER
    global PORT
    global IP_ADDR

    PORT = 6000
    IP_ADDR = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDR,PORT))

    ask_name()

    recv_msg_thread = Thread(target=rcv_msg)
    recv_msg_thread.start()

setup()