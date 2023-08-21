from personal_assistant.sort import sorter_starter
from personal_assistant.addressbook import addressbook_starter
from personal_assistant.notes import notes_main as notes_starter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def menu():

    commands = [" 1  - AddressBook📒", " 2  - NoteBook📋",
                " 3  - Files sorter📂", " 0  - Exit❌"]

    while True:
        
        console = Console()
        table = Table(show_header=True, header_style="bold magenta", width=35, show_lines=True)
        table.add_column("Welcome to main menu", max_width=None)
        table.add_row(" 1  - AddressBook📒")
        table.add_row(" 2  - NoteBook📋")
        table.add_row(" 3  - Files sorter📂")
        table.add_row(" 0  - Exit❌")
        console.print(table)


        imput_console = Console()
        text = "Type number to start:"
        width = 35
        panel = Panel.fit(text,width=width, subtitle_align="center")
        imput_console.print(panel)
        

        user_input = input(">>> ")

        if user_input == '1':
            print("\n✨ AddressBook Started! ✨\n")

            addressbook_starter()
        elif user_input == '2':
            print("\n✨ NoteBook Started! ✨\n")

            notes_starter()
        elif user_input == '3':
            print("\n✨ Files Sorter Started! ✨\n")

            result = sorter_starter()
            print(result)
        elif user_input == '0' or user_input.lower() == "exit":
            print('\nGoodbye!\n')
            break
        else:
            impu_console = Console()
            wrong_table = Table()
            wrong_table.add_column("\nWrong number... Try again...\n")
            imput_console.print(wrong_table)


if __name__ == '__main__':
    menu()
