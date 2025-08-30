from classes import (
    Fore, get_choice, erase_lines,
    change_user_info, notes_mode,
    log_out_message, msvcrt,
    show_user_info, indented_io
)


@indented_io(Fore.MAGENTA + "  | ")
def user_terminal(username, users, notes):
    """
    User terminal.

    Parameters
    ----------
    username: str
        User's username.
    users : pymongo.collection.Collection
        MongoDB collection containing user documents.
    notes : pymongo.collection.Collection
        MongoDB collection containing notes documents.
    """
    user = users.find_one({"username": username})
    print(Fore.CYAN + f"---------- Welcome, {user["username"]}! ----------")
    username_was_updated = False
    while True:
        if username_was_updated:
            erase_lines(1)
            print(
                Fore.CYAN
                + f"---------- Welcome, {user["username"]}! ----------"
            )
            username_was_updated = False

        print(Fore.BLUE + "Select an option:")
        print("\t1. Show your user's information")
        print("\t2. Change your user's information")
        print("\t3. Notes")
        print("\t0. Logout")
        choice = get_choice(5, 0, 3)
        match choice:
            case 1:
                print(
                    Fore.BLUE + "Your choice:", "Show your user's information"
                )
                show_user_info(user=user)
                print("Tap to continue...")
                msvcrt.getch()
                erase_lines(8)
            case 2:
                print(
                    Fore.BLUE
                    + "Your choice:", "Change your user's information"
                )
                updated_user = change_user_info(user=user, users=users)
                if updated_user is not None:
                    if updated_user["username"] != user["username"]:
                        username_was_updated = True
                    user = updated_user
                erase_lines(1)
            case 3:
                notes_mode(user=user, notes=notes)
            case 0:
                log_out_message()
                return
