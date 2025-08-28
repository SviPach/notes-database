from classes import erase_lines, init, Fore, Back, Style
init(autoreset=True)


def get_choice(
        amount_of_lines_to_clear,
        min_choice_possible,
        max_choice_possible
):
    """
    Get the integer permitted choice.

    Parameters
    ----------
    amount_of_lines_to_clear : int
        List of lines (choices + 1) to clear.
    min_choice_possible : int
        Minimum possible choice.
    max_choice_possible : int
        Maximum possible choice.

    Returns
    -------
    int
        Choice.
    """
    erased = False
    while True:
        try:
            choice = int(input(Fore.BLUE + "Your choice: " + Fore.RESET))
            if min_choice_possible <= choice <= max_choice_possible:
                if not erased:
                    erase_lines(1)
                else:
                    erase_lines(2)

                erase_lines(amount_of_lines_to_clear)
                return choice

            if not erased:
                erase_lines(1)
                erased = True
            else:
                erase_lines(2)

            print(Fore.RED + "There is no such a choice!")
        except ValueError:
            if not erased:
                erase_lines(1)
                erased = True
            else:
                erase_lines(2)

            print(Fore.RED + "Please enter the number!")