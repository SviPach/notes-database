from classes import get_choice, erase_lines, Fore


def user_menu(username, users, notes):
    user = users.find_one({"username": username})
    print(Fore.CYAN + f"---------- Welcome, {username}! ----------")
    print(Fore.BLUE + "Select an option:")
    print("\t1. Show your user's information"
          "\n\t2. Change your user's information"
          "\n\t3. Open a note"
          "\n\t0. Logout")
    choice = get_choice(4, 0, 3)
    match choice:
        case 1:
            return
        case 2:
            return
        case 3:
            return
        case 0:
            erase_lines(1)
            print(Fore.GREEN + "Successfully logged out!")
            return