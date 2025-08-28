from classes import(
    Fore, msvcrt, time, DuplicateKeyError,
    ObjectId, erase_lines, get_choice
)


def admin_add_new_user(users):
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
        return
    erase_lines(3)
    print(Fore.GREEN + "New user added!")
    print(Fore.BLUE + "Name:", new_user_username)
    print(Fore.BLUE + "Password:", new_user_password)
    print(Fore.BLUE + "User ID:", new_user_id)
    print("Tap to continue...")
    msvcrt.getch()
    erase_lines(5)

def admin_delete_user(user_to_delete, users):
    if user_to_delete is not None:
        print(Fore.YELLOW + "Are you sure you want to delete:", user_to_delete["username"], "?")
        confirmation = input(Fore.YELLOW + "Type CONFIRM to confirm: " + Fore.RESET)
        if confirmation == "CONFIRM":
            username = user_to_delete["username"]
            users.delete_one({"username": username})
            erase_lines(2)
            print(Fore.GREEN + "User", username, Fore.GREEN + "successfully deleted!")
            time.sleep(2)
            erase_lines(1)
        else:
            erase_lines(2)
            print(Fore.RED + "Deletion not confirmed!")
            time.sleep(2)
            erase_lines(2)

def admin_find_user(users):
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

    if user_found is not None:
        print(Fore.GREEN + "User found!")
    else:
        print(Fore.RED + "There is no such user!")
    time.sleep(1)
    erase_lines(1)
    return user_found