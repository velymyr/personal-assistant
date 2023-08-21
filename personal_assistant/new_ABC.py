from abc import ABC, abstractclassmethod
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class AbstarctCommands(ABC):
    
    @abstractclassmethod
    def main_menu(self):
        ...
    
    @abstractclassmethod
    def address_book_commands(self, command_dict):
        ...

    @abstractclassmethod
    def notes_commands(self, command_dict):
        ...


class RichCommands(AbstarctCommands):
    
    def main_menu(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta", width=35, show_lines=True)
        table.add_column("Welcome to main menu", max_width=None)
        table.add_row(" 1  - AddressBook📒")
        table.add_row(" 2  - NoteBook📋")
        table.add_row(" 3  - Files sorter📂")
        table.add_row(" 0  - Exit❌")
        console.print(table)


        imput_console = Console()
        text = "    Type number to start:"
        panel = Panel(text, width=35)
        imput_console.print(panel)

    def address_book_commands(self,command_dict):
        
        console = Console()
        table = Table(show_header=True, header_style="bold magenta",
                      width=60, show_lines=False)
        table.add_column("Command", max_width=None, no_wrap=False)
        table.add_column("Description", width=20, no_wrap=False)

        for func_name, func in command_dict.items():
            table.add_row(str(func_name), str(func[1]))

        console.print(table)

    def notes_commands(self, command_dict):
        
      console = Console()
      table = Table(show_header=True, header_style="bold magenta", width=60, show_lines=False)
      table.add_column("Command", max_width=None, no_wrap=False)
      table.add_column("Description", width=20, no_wrap=False)

      for func_name, func in command_dict.items():
          table.add_row(str(func_name), str(func[1]))

      console.print(table)