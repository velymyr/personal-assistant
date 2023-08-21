from personal_assistant.sort import sorter_starter
from personal_assistant.addressbook import addressbook_starter
from personal_assistant.notes import notes_main as notes_starter
from rich.console import Console
from rich.panel import Panel
from new_ABC import RichCommands


def menu():

    while True:
        
        main = RichCommands()
        main.main_menu()
        

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
            imput_console = Console()
            text = "  Wrong number... Try again..."
            panel = Panel(text,width=35)
            imput_console.print(panel)


if __name__ == '__main__':
    menu()
1