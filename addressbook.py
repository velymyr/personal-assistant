### Заглушка на адресбук###
# from guesser import main


# def addressbook_starter():
#     main()
import difflib
import inspect
import functools
from rich.console import Console
from rich.table import Table
from main_work_drive import address_book, get_days_to_birthday
from address_book_classes import Record, Name, Phone, Birthday, Email, Address, Note, AddressBook
filename = 'address_book'


def input_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError, TypeError) as e:
            if "takes" in str(e) and "but" in str(e):
                error_message = "Too many arguments provided"
                return error_message
            else:
                error_message = str(e).split(' ')[1]
                return f"Give me {error_message}"
    return wrapper


@input_errors
def add(*args):
    name = Name(input("Name: ")).value.strip()
    phones = Phone().value
    birthday = Birthday().value
    email = Email().value.strip()
    address = Address(input("Address: ")).value
    note = Note(input("Note: ")).value
    record = Record(name=name, phone=phones, birthday=birthday,
                    email=email, address=address, note=note)
    return address_book.add_record(record)


@input_errors
def change():
    ...


# @input_errors
# def save(*args):
#     #filename= filename
#     return address_book.save_address_book()

# @input_errors
# def load(*args):
#     return address_book.load_address_book()


@input_errors
def delete_record(*args):
    name = Name(args[0])
    if name.value in address_book:
        del address_book[name.value]
        return f"Contact '{name}' has been deleted from the address book."
    return f"No contact '{name}' found in the address book."


@input_errors
def remove_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    # print(phone.value)
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.remove_phone(phone.values)
    return f"No contact {name} in address book"


# @input_errors
# def save(*args):
#     if Record.__name__:
#         return save_address_book


# @input_errors
def show_all_address_book():
    if Record.__name__:
        return address_book.show_all_address_book()

def who_has_b_after_n_days():
    days = input(str('After how many days?\n>>> '))
    try:
        n_days = int(days)
    except TypeError:
        return 'This is not a number. Give me a number of days.'
    
    return address_book.who_has_birthday_after_n_days(n_days)


def exit_book():
    pass

def menu():
    pass


command_dict = {
    'add': [add, 'to add contact'],
    'show all': [show_all_address_book, 'to show all contacts'],
    'save': [address_book.save, 'to save address book'],
    'bday': [get_days_to_birthday, 'to get day to birthday'],
    'blist': [who_has_b_after_n_days, 'to show bday boys after N days'],
    'remove': [remove_phone, 'to remove phone from contact'],
    'change': [change, 'to change existing contact'],
    'delete': [delete_record, 'to delete existing contact'],
    'menu': [menu, 'to see list of commands'],
    "0 or exit": [exit_book, 'to exit']
}


def command_handler(user_input, command_dict):
    if user_input in command_dict:
        return command_dict[user_input][0]
    possible_command = difflib.get_close_matches(
        user_input.split()[0], command_dict, cutoff=0.55)
    if possible_command:
        return f'Wrong command. Maybe you mean: {", ".join(possible_command)}'
    else:
        return f'Wrong command.'


def instruction(command_dict):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta", width=60, show_lines=False)
    table.add_column("Command", max_width= None, no_wrap=False)
    table.add_column("Description", width= 20, no_wrap=False)

    for func_name, func in command_dict.items():
        table.add_row(str(func_name), str(func[1]))
    
    console.print(table)


# example of parser user_input
def parser_input(user_input: str, command_dict):  # -> tuple():
    command = None
    arguments = ''

    for key in command_dict.keys():
        if user_input.startswith(key):
            command = key
            arguments = user_input.replace(key, '').strip().split()
            break
    return command, arguments


# def main():
def addressbook_starter():
    filename = "address_book"
    try:
        address_book.load(filename)
        print("Address book loaded from file.")
    except FileNotFoundError:
        print("New address book created.")
        
    print("/n***Hello I`m a contact book.***\n")
    instruction(command_dict)
    
    # print(address_book.congratulate())
    while True:
        user_input = input('>>> ').lower()
        # input 'menu' to show all funcs
        if user_input == 'menu':
            instruction(command_dict)
            # print("Please make a choice")
        elif user_input in ("exit", "0"):
            # del_file_if_empty()
            print('Contact book closed')
            address_book.save()
            break
        else:
            command, arguments = parser_input(user_input, command_dict)
            if command in command_dict:
                result = command_handler(command, command_dict)(*arguments)
            else:
                result = command_handler(user_input, command_dict)
            print(result)


if __name__ == "__main__":
    addressbook_starter()
