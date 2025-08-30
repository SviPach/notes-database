from classes import (
    Fore, Style, time, pymongo,
    MongoClient, admin_terminal,
    user_terminal, erase_lines
)


ERASER_MODE = False


def eraser(mode, reset=False):
    if mode:
        erase_lines(2)
    else:
        erase_lines(1)
    if reset:
        global ERASER_MODE
        ERASER_MODE = False

client = MongoClient()
database = client.mydb
users = database.users
notes = database.notes

users.create_index([('username', pymongo.ASCENDING)], unique=True)

if users.count_documents({"username": "admin"}) == 0:
    users.insert_one({"username": "admin", "password": "admin000"})

print(
    Fore.MAGENTA + Style.BRIGHT
    + "---------- Welcome to the notes database! ----------"
)


def login_terminal(admin_entry=False):
    global ERASER_MODE
    logging_in = True
    first_attempt = True
    while logging_in:
        if first_attempt:
            print(Fore.MAGENTA + "-----Login please:")
            first_attempt = False
        login_username = input(
            Fore.BLUE + "Enter your username('enter' to exit): " + Fore.RESET
        )
        if login_username == "":
            eraser(ERASER_MODE)
            erase_lines(1)
            print(Fore.MAGENTA + Style.BRIGHT + "Exiting...")
            break
        if login_username == "admin" and admin_entry:
            erase_lines(1)
            print(Fore.RED + "Denied")
            time.sleep(2)
            erase_lines(1)
            continue

        user = users.find_one({"username": login_username})

        if user is None:
            eraser(ERASER_MODE)
            ERASER_MODE = True
            print(Fore.RED + "Invalid username! Try again.")
            continue
        else:
            eraser(ERASER_MODE, True)
            while True:
                if admin_entry:
                    erase_lines(1)
                    print(Fore.GREEN + "Login successful!")
                    time.sleep(2)
                    erase_lines(1)
                    user_terminal(login_username, users, notes)
                    first_attempt = True
                    break
                else:
                    login_password = input(
                        Fore.BLUE
                        + "Enter the password('enter' to exit): "
                        + Fore.RESET
                    )
                    if login_password == "":
                        eraser(ERASER_MODE, True)
                        print(Fore.BLUE + "Login canceled!")
                        time.sleep(1)
                        erase_lines(1)
                        break
                    elif user.get("password") != login_password:
                        eraser(ERASER_MODE)
                        ERASER_MODE = True
                        print(Fore.RED + "Invalid password! Try again.")
                        continue
                    else:
                        erase_lines(1)
                        eraser(ERASER_MODE, True)
                        print(Fore.GREEN + "Login successful!")
                        time.sleep(2)
                        erase_lines(1)
                        first_attempt = True
                        if login_username == "admin":
                            admin_login = admin_terminal(users, notes)
                            if admin_login == 1:
                                login_terminal(admin_entry=True)
                                erase_lines(2)
                                print(
                                    Fore.CYAN
                                    + "ADMIN LOGOUT..."
                                )
                                time.sleep(2)
                                erase_lines(1)
                                break
                        else:
                            if admin_entry:
                                user_terminal(login_username, users, notes, enable=True)
                            else:
                                user_terminal(login_username, users, notes, enable=False)
                            break
                        break
login_terminal()
