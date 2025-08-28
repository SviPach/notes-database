from unittest import case

from pymongo.errors import DuplicateKeyError
from classes import get_choice, erase_lines, Fore
import time
import msvcrt
from bson import ObjectId


def admin_menu(users, notes):
    print(Fore.CYAN + "---------- Welcome, admin! ----------")
    while True:
        print(Fore.BLUE + "Select an option:")
        print("\t1. Add new user"
              "\n\t2. Change user's info"
              "\n\t3. Delete a user"
              "\n\t4. Amount of users"
              "\n\t5. Find a user"
              "\n\t0. Logout")
        choice = get_choice(7, 0, 5)
        match choice:
            case 1:
                print(Fore.BLUE + "Your choice:", "Add new user")
                new_user_username = input(Fore.BLUE + "\tEnter a username: " + Fore.RESET)
                new_user_password = input(Fore.BLUE + "\tEnter a password: " + Fore.RESET)
                try:
                    new_user_id = users.insert_one({"username": new_user_username, "password": new_user_password}).inserted_id
                except DuplicateKeyError:
                    erase_lines(1)
                    print(Fore.RED + "User with this username already exists!")
                    print("Tap to continue...")
                    msvcrt.getch()
                    erase_lines(4)
                    continue
                erase_lines(3)
                print(Fore.GREEN + "New user added!")
                print(Fore.BLUE + "Name:", new_user_username)
                print(Fore.BLUE + "Password:", new_user_password)
                print(Fore.BLUE + "User ID:", new_user_id)
                print("Tap to continue...")
                msvcrt.getch()
                erase_lines(5)
            case 2:
                print(Fore.BLUE + "Your choice:", "Change user's info")
                print(Fore.BLUE + "Find a user by:")
                print("\t1. Username"
                      "\n\t2. User ID"
                      "\n\t0. Cancel the operation")
                choice = get_choice(4, 0, 2)
                if choice == 0:
                    erase_lines(1)
                    print(Fore.BLUE + "Operation cancelled!")
                    time.sleep(2)
                    erase_lines(1)
                else:
                    user_found = find_user_by(users, choice)
                    show_user_info(user_found)
                    show_user_info_static(user_found)
                    if user_found is None:
                        continue

                    print(Fore.BLUE + "What to change:")
                    print("\t1. Username"
                          "\n\t2. Password"
                          "\n\t0. Cancel the operation")
                    choice = get_choice(4, 0, 2)
                    match choice:
                        case 1:
                            new_username = input(Fore.BLUE + "Enter a new username: " + Fore.RESET)
                            print(Fore.YELLOW + "Are you sure you want to change this user's username?")
                            change_user_info(users, user_found, "username", new_username)
                            erase_lines(3)
                        case 2:
                            new_password = input(Fore.BLUE + "Enter a new password: " + Fore.RESET)
                            print(Fore.YELLOW + "Are you sure you want to change this user's password?")
                            change_user_info(users, user_found, "password", new_password)
                            erase_lines(3)
                        case 0:
                            erase_lines(1)
                            print(Fore.BLUE + "Operation cancelled!")
                            time.sleep(2)
                            erase_lines(1)
            case 3:
                print(Fore.BLUE + "Your choice:", "Delete a user")
                print(Fore.BLUE + "Delete a user by:")
                print("\t1. Username"
                      "\n\t2. User ID"
                      "\n\t0. Cancel the operation")
                choice = get_choice(4, 0, 2)
                if choice == 0:
                    erase_lines(1)
                    print(Fore.BLUE + "Operation cancelled!")
                    time.sleep(2)
                    erase_lines(1)
                else:
                    user_to_delete = find_user_by(users, choice)

                    if user_to_delete is not None:
                        erase_lines(1)
                        print(Fore.YELLOW + "Are you sure you want to delete:", user_to_delete["username"], "?")
                        confirmation = input(Fore.YELLOW + "Type DELETE to confirm: " + Fore.RESET)
                        if confirmation == "DELETE":
                            username = user_to_delete["username"]
                            users.delete_one({"username": username})
                            erase_lines(3)
                            print(Fore.GREEN + "User", username, Fore.GREEN + "successfully deleted!")
                            time.sleep(2)
                            erase_lines(1)
                        else:
                            erase_lines(2)
                            print(Fore.RED + "Deletion not confirmed!")
                            time.sleep(2)
                            erase_lines(2)
                    else:
                        erase_lines(2)
                        print(Fore.RED + "There is no such user!")
                        time.sleep(2)
                        erase_lines(1)
            case 4:
                print(Fore.BLUE + "Amount of users:", users.count_documents({}))
                print("Tap to continue...")
                msvcrt.getch()
                erase_lines(2)
            case 5:
                print(Fore.BLUE + "Your choice:", "Find a user")
                print(Fore.BLUE + "Find a user by:")
                print("\t1. Username"
                      "\n\t2. User ID"
                      "\n\t0. Cancel the operation")
                choice = get_choice(4, 0, 2)
                if choice == 0:
                    erase_lines(1)
                    print(Fore.BLUE + "Operation cancelled!")
                    time.sleep(2)
                    erase_lines(1)
                else:
                    user_found = find_user_by(users, choice)
                    show_user_info(user_found)
            case 0:
                erase_lines(1)
                print(Fore.GREEN + "Successfully logged out!")
                time.sleep(2)
                erase_lines(1)
                return

def find_user_by(users, choice):
    user_found = None
    if choice == 1:
        while True:
            username_to_find = input(Fore.BLUE + "Please enter a username: " + Fore.RESET)
            if username_to_find == "admin":
                erase_lines(1)
                print(Fore.RED + "No permission.")
                time.sleep(2)
                erase_lines(1)
                continue
            user_found = users.find_one({"username": username_to_find})
            break
    if choice == 2:
        id_to_find = input(Fore.BLUE + "Please enter a user's ID: " + Fore.RESET)
        user_found = users.find_one({"_id": ObjectId(id_to_find)})
    return user_found

def show_user_info(user):
    if user is not None:
        erase_lines(2)
        print(Fore.GREEN + "User found!")
        time.sleep(1)
        erase_lines(1)
        print(Fore.BLUE + "User ID:", user["_id"])
        print(Fore.BLUE + "Username:", user["username"])
        print(Fore.BLUE + "Password:", user["password"])
        print("Tap to continue...")
        msvcrt.getch()
        erase_lines(4)
    else:
        erase_lines(2)
        print(Fore.RED + "There is no such user!")
        time.sleep(2)
        erase_lines(1)

def show_user_info_static(user):
    if user is not None:
        print(Fore.BLUE + "\tUser ID:", user["_id"])
        print(Fore.BLUE + "\tUsername:", user["username"])
        print(Fore.BLUE + "\tPassword:", user["password"])

def change_user_info(users, user, attribute, new_value):
    print("\t" + user[attribute] + " -> " + new_value)
    confirmation = input(Fore.YELLOW + "Type CONFIRM to confirm: " + Fore.RESET)
    if confirmation == "CONFIRM":
        if attribute == "username":
            user_check = users.find_one({"username": new_value})
            if user_check is not None:
                print(Fore.RED + "User with this username already exists!")
                return
        users.update_one({"_id": user["_id"]}, {"$set": {attribute: new_value}})
        erase_lines(4)
        print(Fore.GREEN + f"{attribute} successfully changed!")
        time.sleep(2)
        erase_lines(1)
    else:
        erase_lines(3)
        print(Fore.RED + "Change not confirmed!")
        time.sleep(2)
        erase_lines(2)