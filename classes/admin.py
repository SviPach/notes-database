from classes import get_choice, erase_lines, Fore


def admin_menu(users, notes):
    print(Fore.CYAN + "---------- Welcome, admin! ----------")
    print(Fore.BLUE + "Select an option:")
    print("\t1. Add new user"
          "\n\t2. Change user's info"
          "\n\t3. Delete a user"
          "\n\t4. Amount of users"
          "\n\t0. Logout")
    choice = get_choice(6, 0, 4)
    match choice:
        case 1:
            return
        case 2:
            return
        case 3:
            return
        case 4:
            return
        case 0:
            erase_lines(1)
            print(Fore.GREEN + "Successfully logged out!")
            return