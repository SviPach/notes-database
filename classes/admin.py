from classes import (
    Fore, msvcrt, get_choice, erase_lines,
    change_user_info, log_out_message,
    admin_find_user, admin_delete_user,
    admin_add_new_user, show_user_info,
    admin_restore_deleted_user, Style,
    time
)


def admin_terminal(users, notes):
    """
    Admin terminal.

    Parameters
    ----------
    users : pymongo.collection.Collection
        MongoDB collection containing user documents.
    notes : pymongo.collection.Collection
        MongoDB collection containing notes documents.

    Returns
    -------
    int
        Status code:
            0 — normal exit from admin terminal
            1 — admin requested login as another user
    """
    print(Fore.CYAN + "---------- Welcome, admin! ----------")
    deleted_user = []
    while True:
        print(Fore.BLUE + "Select an option:")
        print("\t1. Add new user"
              "\n\t2. Change user's info"
              "\n\t3. Delete a user"
              "\n\t4. List of users"
              "\n\t5. Find a user"
              "\n\t6. Admin login terminal"
              "\n\t7. Restore last deleted user"
              "\n\t0. Logout")
        choice = get_choice(9, 0, 7)
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
                deleted_user = admin_delete_user(user_to_delete, users, notes)
                erase_lines(1)
            case 4:
                users_amount = users.count_documents({})
                print(
                    Fore.BLUE + "Amount of users:", users_amount
                )
                print(Fore.BLUE + "Users:")
                users_output = users.find({}, {"username": 1, "_id": 1})
                for user_output in users_output:
                    print(
                        f"\t{user_output["username"]}:",
                        Fore.CYAN + str(user_output["_id"])
                    )
                print("Tap to continue...")
                msvcrt.getch()
                erase_lines(users_amount + 3)
            case 5:
                print(Fore.BLUE + "Your choice:", "Find a user")
                user_found = admin_find_user(users)
                show_user_info(user_found)
                print("Tap to continue...")
                msvcrt.getch()
                erase_lines(8)
            case 6:
                erase_lines(1)
                print(Fore.CYAN + "Logging in as admin...")
                time.sleep(2)
                erase_lines(1)
                print(
                    Fore.CYAN + Style.BRIGHT
                    + "---------- ADMIN LOGIN ----------"
                )
                return 1
            case 7:
                print(Fore.BLUE + "Your choice:", "Restore last deleted user")
                result = admin_restore_deleted_user(deleted_user, users, notes)
                if result == 1:
                    deleted_user = []
                erase_lines(1)
            case 0:
                log_out_message()
                return 0
