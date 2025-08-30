from classes import (
    Fore, time, DuplicateKeyError,
    ObjectId, erase_lines, get_choice,
    datetime, msvcrt, show_user_info
)


def admin_add_new_user(users):
    """
    Add a new user to the database.

    Parameters
    ----------
    users : pymongo.collection.Collection
        MongoDB collection containing user documents.
    """
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
    while True:
        new_user_password = input(
            Fore.BLUE + "\tEnter a password: " + Fore.RESET
        )
        if new_user_password == "":
            erase_lines(1)
            print(Fore.RED + "Password is empty! Try again!")
            time.sleep(2)
            erase_lines(1)
            continue
        else:
            break
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
    show_user_info(user=new_user)
    print("Tap to continue...")
    msvcrt.getch()
    erase_lines(8)


def admin_delete_user(user_to_delete, users, notes):
    """
    Delete a user from the database.

    Parameters
    ----------
    user_to_delete : dict
        A MongoDB user document we want to delete.
    users : pymongo.collection.Collection
        MongoDB collection containing user documents.
    notes : pymongo.collection.Collection
        MongoDB collection containing notes documents.

    Returns
    -------
    list or None
        Information about user and his notes if deleted, otherwise None.
    """
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
            save_user = user_to_delete.copy()
            save_user_notes = list(
                notes.find(
                    {"user_id": ObjectId(user_to_delete["_id"])}
                )
            )
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
            return [save_user, save_user_notes]
        else:
            erase_lines(3)
            print(Fore.RED + "Deletion not confirmed!")
            time.sleep(2)
            erase_lines(1)
            return None


def admin_find_user(users):
    """
    Find a user in the database.

    Parameters
    ----------
    users : pymongo.collection.Collection
        MongoDB collection containing user documents.

    Returns
    -------
    dict or None
        The user dictionary if found, otherwise None.
    """
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


def admin_restore_deleted_user(deleted_user, users, notes):
    """
    Restore last deleted user in the current session.

    Parameters
    ----------
    deleted_user : dict
        A previously deleted MongoDB user document (saved before deletion).
    users : pymongo.collection.Collection
        MongoDB collection containing user documents.
    notes : pymongo.collection.Collection
        MongoDB collection containing notes documents.

    Returns
    -------
    int or None
        Returns 1 if deleted user was successfully restored, otherwise None.
    """
    if len(deleted_user) != 0:
        while users.find_one({"username": deleted_user[0]["username"]}):
            new_username = input(
                Fore.YELLOW
                + "Impossible to restore. Need a new username: "
                + Fore.RESET
            )
            if users.find_one({"username": new_username}):
                erase_lines(1)
                print(
                    Fore.RED
                    + "Username already exists."
                      "Try another one."
                )
                time.sleep(2)
                erase_lines(1)
                continue
            else:
                deleted_user[0]["username"] = new_username
                break

        user_to_restore = deleted_user[0].copy()
        notes_to_restore = deleted_user[1]

        print(
            Fore.YELLOW
            + "Are you sure you want to restore:",
            user_to_restore["username"], '?'
        )
        confirmation = input(
            Fore.YELLOW + "Type CONFIRM to confirm: " + Fore.RESET
        )
        if confirmation == "CONFIRM":
            user_to_restore.pop("_id", None)
            new_user_id = users.insert_one(user_to_restore).inserted_id
            for note in notes_to_restore:
                note.pop("_id", None)
                note["user_id"] = new_user_id
                notes.insert_one(note)
            erase_lines(2)
            print(Fore.GREEN + "User restored.")
            time.sleep(2)
            erase_lines(1)
            return 1
        else:
            erase_lines(2)
            print(Fore.RED + "User restore not confirmed!")
            time.sleep(2)
            erase_lines(1)
            return None
    else:
        print(Fore.RED + "You have not deleted any user in this session.")
        time.sleep(2)
        erase_lines(1)
        return None
