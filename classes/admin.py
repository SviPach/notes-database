from classes import (
    Fore, msvcrt, get_choice, erase_lines,
    show_user_info, change_user_info,
    log_out_message, admin_find_user,
    admin_delete_user, admin_add_new_user
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
                admin_add_new_user(users)
            case 2:
                print(Fore.BLUE + "Your choice:", "Change user's information")
                user_found = admin_find_user(users)
                change_user_info(user_found, users)
                erase_lines(1)
            case 3:
                print(Fore.BLUE + "Your choice:", "Delete a user")
                user_to_delete = admin_find_user(users)
                admin_delete_user(user_to_delete, users)
                erase_lines(1)
            case 4:
                print(Fore.BLUE + "Amount of users:", users.count_documents({}))
                print("Tap to continue...")
                msvcrt.getch()
                erase_lines(2)
            case 5:
                print(Fore.BLUE + "Your choice:", "Find a user")
                user_found = admin_find_user(users)
                show_user_info(user_found)
                erase_lines(1)
            case 0:
                log_out_message()
                return

