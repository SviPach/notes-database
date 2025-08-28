from classes import (
    get_choice, erase_lines, Fore, show_user_info,
    change_user_info, DuplicateKeyError, time, msvcrt, ObjectId
)


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
                    change_user_info(user_found, users)
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
            erase_lines(2)
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

    print(Fore.GREEN + "User found!")
    time.sleep(1)
    erase_lines(1)
    return user_found