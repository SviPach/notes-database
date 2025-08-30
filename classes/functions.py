from classes import (
    erase_lines, get_choice, Fore, prompt,
    time, datetime, ObjectId
)


def show_user_info(user):
    """
    Show user info.

    Parameters
    ----------
    user : dict
        A MongoDB document representing a user (as returned by find_one()).
    """
    if user is not None:
        print(Fore.BLUE + "\tUser ID:", user["_id"])
        print(Fore.BLUE + "\tUsername:", user["username"])
        print(Fore.BLUE + "\tPassword:", user["password"])
        print(Fore.BLUE + "\tAge:", user["age"])
        print(Fore.BLUE + "\tE-mail:", user["email"])
        print(Fore.BLUE + "\tDate created:", user["date_created"])


def change_user_info(user, users):
    """
    A menu of options to change user info.

    Parameters
    ----------
    user : dict
        A MongoDB document representing a user (as returned by find_one()).
    users : pymongo.collection.Collection
        MongoDB collection containing user documents.

    Returns
    -------
    dict or None
        User to update document if changes were applied, otherwise None.
    """
    if user is not None:
        show_user_info(user=user)
        print(Fore.BLUE + "What to change:")
        print("\t1. Username")
        print("\t2. Password")
        print("\t3. Age")
        print("\t4. E-mail")
        print("\t0. Cancel the operation")
        choice = get_choice(6, 0, 4)
        match choice:
            case 1:
                new_username = input(
                    Fore.BLUE + "Enter a new username: " + Fore.RESET
                )
                forbidden = set('!@#$%^&*()+={}[]|\\:;"\'<>,.?/~` ')
                if (
                        any(c in forbidden for c in new_username)
                        or
                        new_username == ""
                ):
                    erase_lines(7)
                    print(Fore.RED + "Username contains forbidden characters!")
                    time.sleep(2)
                    erase_lines(1)
                    return None
                else:
                    erase_lines(7)
                    updated_user = change_user_info_db(
                        users=users,
                        user=user,
                        attribute="username",
                        new_value=new_username
                    )
                    return updated_user
            case _ if choice in range(2, 5):
                attribute = ""
                if choice == 2:
                    attribute = "password"
                elif choice == 3:
                    attribute = "age"
                elif choice == 4:
                    attribute = "email"

                new_value = input(
                    Fore.BLUE + f"Enter a new {attribute}: " + Fore.RESET
                )
                erase_lines(7)
                updated_user = change_user_info_db(
                    users=users,
                    user=user,
                    attribute=attribute,
                    new_value=new_value
                )
                return updated_user
            case 0:
                erase_lines(6)
                print(Fore.GREEN + "Operation cancelled!")
                time.sleep(2)
                erase_lines(1)
                return None
    else:
        return None


def change_user_info_db(users, user, attribute, new_value):
    """
    Change user's information in database.

    Parameters
    ----------
    users : pymongo.collection.Collection
        MongoDB collection containing user documents.
    user : dict
        A MongoDB document representing a user (as returned by find_one()).
    attribute : str
        Attribute to change.
    new_value : str
        New value of the attribute.

    Returns
    -------
    dict or None
        Updated user document if changes were applied, otherwise None.
    """
    print(
        Fore.YELLOW
        + f"Are you sure you want to change this user's {attribute}?"
    )
    if user[attribute] is None:
        print("\tNew value will be:", new_value)
    else:
        print("\t" + user[attribute] + " -> " + new_value)
    confirmation = input(
        Fore.YELLOW + "Type CONFIRM to confirm: " + Fore.RESET
    )
    if confirmation == "CONFIRM":
        if attribute == "username":
            user_check = users.find_one({"username": new_value})
            if user_check is not None:
                erase_lines(3)
                print(Fore.RED + "User with this username already exists!")
                time.sleep(2)
                erase_lines(1)
                return None
        users.update_one(
            {"_id": user["_id"]}, {"$set": {attribute: new_value}}
        )
        erase_lines(3)
        print(Fore.GREEN + f"{attribute} successfully changed!")
        time.sleep(2)
        erase_lines(1)
        updated_user = users.find_one({"_id": user["_id"]})
        return updated_user
    else:
        erase_lines(3)
        print(Fore.RED + "Change not confirmed!")
        time.sleep(2)
        erase_lines(1)
        return None


def notes_mode(user, notes):
    """
    User's notes mode.

    Parameters
    ----------
    user : dict
        A MongoDB document representing a user (as returned by find_one()).
    notes : pymongo.collection.Collection
        MongoDB collection containing notes documents.
    """
    notes_available = list(notes.find({"user_id": ObjectId(user["_id"])}))
    if notes_available is not None:
        print(Fore.BLUE + "Choose a note:")
        i = 1
        for note in notes_available:
            print(f"\t{i}. {note["name"]}")
            i += 1
        print("\t0. Create a new note")
        print("\t-1. Cancel the operation")
        notes_count = notes.count_documents({"user_id": user["_id"]})
        choice = get_choice(notes_count + 3, -1, notes_count)
        if choice == -1:
            print(Fore.GREEN + "Operation cancelled!")
            time.sleep(2)
            erase_lines(1)

        if choice == 0:
            note_name = input(
                Fore.BLUE + "Choose a name for the new note: " + Fore.RESET
            )
            erase_lines(1)
            if notes.find_one(
                    {"name": note_name, "user_id": ObjectId(user["_id"])}
            ) is not None:
                print(Fore.RED + "You already have a note with that name!")
                time.sleep(2)
                erase_lines(1)
            else:
                notes.insert_one(
                    {
                        "user_id": ObjectId(user["_id"]),
                        "name": note_name,
                        "content": "",
                        "date_created": datetime.datetime.now()
                    }
                )
                print(Fore.GREEN + "New note created!")
                time.sleep(2)
                erase_lines(1)
        else:
            note_chosen = notes_available[choice - 1]
            if note_chosen is not None:
                print(Fore.BLUE + "Choose an action:")
                print("\t1. Open")
                print("\t2. Rename")
                print("\t3. Delete")
                print("\t0. Exit")
                choice = get_choice(5, 0, 3)
                match choice:
                    case 1:
                        print(
                            Fore.BLUE
                            + f"---------- {note_chosen["name"]}:"
                        )
                        print(
                            Fore.BLUE
                            + "----- Use Alt+Enter or Ctrl+Z+Enter to exit"
                        )
                        content = prompt(
                            default=note_chosen["content"], multiline=True
                        )
                        notes.update_one(
                            {"_id": ObjectId(note_chosen["_id"])},
                            {"$set": {"content": content}}
                        )
                        lines_amount = content.count('\n') + 1
                        erase_lines(lines_amount+2)
                        print(Fore.GREEN + "Note saved!")
                        time.sleep(2)
                        erase_lines(1)
                    case 2:
                        print(Fore.BLUE + f"---------- {note_chosen["name"]}:")
                        new_name = input(
                            Fore.BLUE + "Enter new name: " + Fore.RESET
                        )
                        print("\t" + note_chosen["name"] + " -> " + new_name)
                        confirmation = input(
                            Fore.YELLOW
                            + "Type CONFIRM to confirm: "
                            + Fore.RESET
                        )
                        if confirmation == "CONFIRM":
                            notes.update_one(
                                {"_id": ObjectId(note_chosen["_id"])},
                                {"$set": {"name": new_name}}
                            )
                            erase_lines(4)
                            print(Fore.GREEN + "Name successfully changed!")
                            time.sleep(2)
                            erase_lines(1)
                        else:
                            erase_lines(4)
                            print(Fore.RED + "Change not confirmed!")
                            time.sleep(2)
                            erase_lines(1)
                    case 3:
                        print(Fore.BLUE + f"---------- {note_chosen["name"]}:")
                        print(
                            Fore.YELLOW
                            + "Are you sure you want to delete this note?"
                        )
                        confirmation = input(
                            Fore.YELLOW
                            + "Type CONFIRM to confirm: "
                            + Fore.RESET
                        )
                        if confirmation == "CONFIRM":
                            notes.delete_one(
                                {"_id": ObjectId(note_chosen["_id"])}
                            )
                            erase_lines(3)
                            print(Fore.GREEN + "Note successfully deleted!")
                            time.sleep(2)
                            erase_lines(1)
                        else:
                            erase_lines(3)
                            print(Fore.RED + "Deletion not confirmed!")
                            time.sleep(2)
                            erase_lines(1)
                    case 4:
                        print(Fore.GREEN + "Closed!")
                        time.sleep(2)
                        erase_lines(1)
                        return
            else:
                print(Fore.RED + "Note not found!")
                time.sleep(2)
                erase_lines(1)


def log_out_message():
    """ Message when logging out. """
    erase_lines(1)
    print(Fore.GREEN + "Successfully logged out!")
    time.sleep(2)
    erase_lines(1)
