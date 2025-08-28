import pymongo
from pymongo import MongoClient
import datetime
from classes import admin_menu, user_menu, erase_lines, Fore, Style


global ERASER_MODE

def eraser(mode, reset=False):
    if mode:
        erase_lines(2)
    else:
        erase_lines(1)
    if reset:
        global ERASER_MODE
        ERASER_MODE = False


myClient = MongoClient()
db = myClient.mydb
users = db.users
notes = db.notes

users.create_index([('username', pymongo.ASCENDING)], unique=True)

if users.count_documents({"username": "admin"}) == 0:
    users.insert_one({"username": "admin", "password": "admin000"})

print(Fore.MAGENTA + Style.BRIGHT + "---------- Welcome to the notes database! ----------")
print(Fore.MAGENTA + "-----Login please:")

logging_in = True
ERASER_MODE = False
while logging_in:
    login_username = input(Fore.BLUE + "Enter your username('enter' to exit): ")
    if login_username == "":
        eraser(ERASER_MODE)
        print(Fore.MAGENTA + Style.BRIGHT + "Exiting...")
        break

    user = users.find_one({"username": login_username})

    if user is None:
        eraser(ERASER_MODE)
        ERASER_MODE = True
        print(Fore.RED + "Invalid username! Try again.")
        continue
    else:
        eraser(ERASER_MODE, True)
        while True:
            login_password = input(Fore.BLUE + "Enter the password('enter' to exit): ")
            if login_password == "":
                eraser(ERASER_MODE, True)
                print(Fore.BLUE + "Login canceled!")
                break
            elif user.get("password") != login_password:
                eraser(ERASER_MODE)
                ERASER_MODE = True
                print(Fore.RED + "Invalid password! Try again.")
                continue
            else:
                eraser(ERASER_MODE, True)
                erase_lines(1)
                print(Fore.GREEN + "Login successful!")
                if login_username == "admin":
                    admin_menu(users, notes)
                else:
                    user_menu(login_username, users, notes)

                break