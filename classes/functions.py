from classes import (
    erase_lines, get_choice, Fore, prompt,
    time, datetime, ObjectId, msvcrt
)


def show_user_info(user):
    if user is not None:
        print(Fore.BLUE + "User ID:", user["_id"])
        print(Fore.BLUE + "Username:", user["username"])
        print(Fore.BLUE + "Password:", user["password"])
        print("Tap to continue...")
        msvcrt.getch()
        erase_lines(4)

def show_user_info_static(user):
    if user is not None:
        print(Fore.BLUE + "\tUser ID:", user["_id"])
        print(Fore.BLUE + "\tUsername:", user["username"])
        print(Fore.BLUE + "\tPassword:", user["password"])

def change_user_info(user, users):
    if user is None:
        print(Fore.RED + "User not found!")
        return None
    show_user_info_static(user)
    print(Fore.BLUE + "What to change:")
    print("\t1. Username"
          "\n\t2. Password"
          "\n\t0. Cancel the operation")
    choice = get_choice(4, 0, 2)
    match choice:
        case 1:
            new_username = input(Fore.BLUE + "Enter a new username: " + Fore.RESET)
            print(Fore.YELLOW + "Are you sure you want to change this user's username?")
            updated_user = change_user_info_db(users, user, "username", new_username)
            erase_lines(3)
            return updated_user
        case 2:
            new_password = input(Fore.BLUE + "Enter a new password: " + Fore.RESET)
            print(Fore.YELLOW + "Are you sure you want to change this user's password?")
            updated_user = change_user_info_db(users, user, "password", new_password)
            erase_lines(3)
            return updated_user
        case 0:
            erase_lines(1)
            print(Fore.BLUE + "Operation cancelled!")
            time.sleep(2)
            erase_lines(1)
            return None

def change_user_info_db(users, user, attribute, new_value):
    print("\t" + user[attribute] + " -> " + new_value)
    confirmation = input(Fore.YELLOW + "Type CONFIRM to confirm: " + Fore.RESET)
    if confirmation == "CONFIRM":
        if attribute == "username":
            user_check = users.find_one({"username": new_value})
            if user_check is not None:
                print(Fore.RED + "User with this username already exists!")
                return None
        users.update_one({"_id": user["_id"]}, {"$set": {attribute: new_value}})
        erase_lines(4)
        print(Fore.GREEN + f"{attribute} successfully changed!")
        time.sleep(2)
        erase_lines(1)
        updated_user = users.find_one({"_id": user["_id"]})
        return updated_user
    else:
        erase_lines(3)
        print(Fore.RED + "Change not confirmed!")
        time.sleep(2)
        erase_lines(2)
        return None

def notes_mode(user, notes):
    notes_available = list(notes.find({"user_id": ObjectId(user["_id"])}))
    if notes_available is not None:
        print(Fore.BLUE + "Choose a note:")
        i = 1
        for note in notes_available:
            print(f"\t{i}. {note["name"]}")
            i += 1
        print("\t0. Create a new note"
              "\n\t-1. Cancel the operation")
        notes_count = notes.count_documents({"user_id": user["_id"]})
        choice = get_choice(notes_count + 3, -1, notes_count)
        if choice == -1:
            print(Fore.BLUE + "Operation cancelled!")
            time.sleep(2)
            erase_lines(1)

        if choice == 0:
            note_name = input(Fore.BLUE + "Choose a name for the new note: " + Fore.RESET)
            erase_lines(1)
            if notes.find_one({"name": note_name, "user_id": ObjectId(user["_id"])}) is not None:
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
                print("\t1. Open"
                      "\n\t2. Rename"
                      "\n\t3. Delete"
                      "\n\t0. Exit")
                choice = get_choice(5, 0, 3)
                match choice:
                    case 1:
                        print(Fore.BLUE + f"---------- {note_chosen["name"]}:")
                        print(Fore.BLUE + "----- Use Alt+Enter or Ctrl+Z+Enter to exit")
                        content = prompt(default=note_chosen["content"], multiline=True)
                        notes.update_one({"_id": ObjectId(note_chosen["_id"])}, {"$set": {"content": content}})
                        lines_amount = content.count('\n') + 1
                        erase_lines(lines_amount+2)
                        print(Fore.GREEN + "Note saved!")
                        time.sleep(2)
                        erase_lines(1)
                    case 2:
                        print(Fore.BLUE + f"---------- {note_chosen["name"]}:")
                        new_name = input(Fore.BLUE + "Enter new name: " + Fore.RESET)
                        print("\t" + note_chosen["name"] + " -> " + new_name)
                        confirmation = input(Fore.YELLOW + "Type CONFIRM to confirm: " + Fore.RESET)
                        if confirmation == "CONFIRM":
                            notes.update_one({"_id": ObjectId(note_chosen["_id"])}, {"$set": {"name": new_name}})
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
                        print(Fore.YELLOW + "Are you sure you want to delete this note?")
                        confirmation = input(Fore.YELLOW + "Type CONFIRM to confirm: " + Fore.RESET)
                        if confirmation == "CONFIRM":
                            notes.delete_one({"_id": ObjectId(note_chosen["_id"])})
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
    erase_lines(1)
    print(Fore.GREEN + "Successfully logged out!")
    time.sleep(2)
    erase_lines(1)