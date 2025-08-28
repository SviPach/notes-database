from classes import (
    Fore, get_choice, erase_lines, show_user_info,
    change_user_info, notes_mode, log_out_message
)


def user_menu(username, users, notes):
    user = users.find_one({"username": username})
    print(Fore.CYAN + f"---------- Welcome, {user["username"]}! ----------")
    username_was_updated = False
    while True:
        if username_was_updated:
            erase_lines(1)
            print(Fore.CYAN + f"---------- Welcome, {user["username"]}! ----------")
            username_was_updated = False

        print(Fore.BLUE + "Select an option:")
        print("\t1. Show your user's information"
              "\n\t2. Change your user's information"
              "\n\t3. Notes"
              "\n\t0. Logout")
        choice = get_choice(5, 0, 3)
        match choice:
            case 1:
                show_user_info(user)
            case 2:
                print(Fore.BLUE + "Your choice:", "Change your user's information")
                updated_user = change_user_info(user, users)
                if updated_user is not None:
                    if updated_user["username"] != user["username"]:
                        username_was_updated = True
                    user = updated_user
                erase_lines(1)
            case 3:
                notes_mode(user, notes)
            case 0:
                log_out_message()
                return