from classes import (
    Fore, time, DuplicateKeyError,
    ObjectId, erase_lines, get_choice,
    datetime, msvcrt, show_user_info
)


def admin_add_new_user(users):
    print(Fore.BLUE + "Your choice:", "Add new user")
    new_user_username = input(Fore.BLUE + "\tEnter a username: " + Fore.RESET)
    forbidden = set('!@#$%^&*()+={}[]|\\:;"\'<>,.?/~` ')
    if (
            any(c in forbidden for c in new_user_username)
            or
            new_user_username == ""
    ):
        print(Fore.RED + "Username contains forbidden characters!")
        time.sleep(2)
        erase_lines(3)
        return
    new_user_password = input(Fore.BLUE + "\tEnter a password: " + Fore.RESET)
    new_user_date_created = datetime.datetime.now()
    try:
        new_user_id = users.insert_one(
            {
                "username": new_user_username,
                "password": new_user_password,
                "age": None,
                "email": None,
                "date_birth": None,
                "date_created": new_user_date_created
            }
        ).inserted_id
    except DuplicateKeyError:
        erase_lines(3)
        print(Fore.RED + "User with this username already exists!")
        time.sleep(2)
        erase_lines(1)
        return
    erase_lines(3)
    new_user = users.find_one({"_id": ObjectId(new_user_id)})
    print(Fore.GREEN + "New user added:")
    show_user_info(new_user)
    print("Tap to continue...")
    msvcrt.getch()
    erase_lines(8)


def admin_delete_user(user_to_delete, users, notes):
    if user_to_delete is not None:
        print(
            Fore.YELLOW
            + "Are you sure you want to delete:",
            user_to_delete["username"], "?"
        )
        print(Fore.YELLOW + "User's notes will be deleted!")
        confirmation = input(
            Fore.YELLOW + "Type CONFIRM to confirm: " + Fore.RESET
        )
        if confirmation == "CONFIRM":
            notes.delete_many({"user_id": ObjectId(user_to_delete["_id"])})

            username = user_to_delete["username"]
            users.delete_one({"username": username})
            erase_lines(3)
            print(
                Fore.GREEN + "User",
                username,
                Fore.GREEN + "successfully deleted!"
            )
            time.sleep(2)
            erase_lines(1)
        else:
            erase_lines(3)
            print(Fore.RED + "Deletion not confirmed!")
            time.sleep(2)
            erase_lines(1)


def admin_find_user(users):
    print(Fore.BLUE + "Find a user by:")
    print("\t1. Username"
          "\n\t2. User ID"
          "\n\t0. Cancel the operation")
    choice = get_choice(4, 0, 2)
    if choice == 0:
        print(Fore.GREEN + "Operation cancelled!")
        time.sleep(2)
        erase_lines(1)
        return None

    user_found = None
    if choice == 1:
        while True:
            username_to_find = input(
                Fore.BLUE + "Please enter a username: " + Fore.RESET
            )
            erase_lines(1)
            if username_to_find == "admin":
                print(Fore.RED + "No permission.")
                time.sleep(2)
                erase_lines(1)
                continue
            user_found = users.find_one({"username": username_to_find})
            break
    if choice == 2:
        id_to_find = input(
            Fore.BLUE + "Please enter a user's ID: " + Fore.RESET
        )
        erase_lines(1)
        user_found = users.find_one({"_id": ObjectId(id_to_find)})

    if user_found is not None:
        print(Fore.GREEN + "User found!")
    else:
        print(Fore.RED + "There is no such user!")
    time.sleep(2)
    erase_lines(1)
    return user_found
