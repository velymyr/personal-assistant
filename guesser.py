import difflib
import inspect
import functools
from main_work_drive import load_address_book, save_address_book, parser, address_book, exit_command
from address_book_classes import Record, Name, Phone


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
                error_message = str(e).split(':')[1]
                return f"Give me {error_message}"
    return wrapper


@input_errors
def add(*args):
    ...


@input_errors
def change():
    ...


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
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.remove_phone(phone)
    return f"No contact {name} in address book"


# @input_errors
# def save(*args):
#     if Record.__name__:
#         return save_address_book


@input_errors
def show_all_command(*args):
    if Record.__name__:
        return address_book


command_dict = {
    'add': [add, 'add contact'],
    'show': [show_all_command, 'show'],
    # 'save': [save_address_book, 'save address book'],
    'remove phone': [remove_phone, 'remove phone from contacts'],
    'change': [change, 'change existing contact'],
    'delete contact': [delete_record, 'delete contact']
}


# use difflib.get_close_matches for guess the command. Usually cutoff=0.6, but maybe better to set 0.4-0.5 to wider guessing
def command_handler(user_input, command_dict):
    if user_input in command_dict:
        return command_dict[user_input][0]
    possible_command = difflib.get_close_matches(
        user_input.split()[0], command_dict, cutoff=0.45)
    if possible_command:
        return f'An unknown command. Maybe you mean: {", ".join(possible_command)}'
    else:
        return f'An unknown command.'


# like welcome message - to show all funcs for contact book etc.
def instruction(command_dict):
    result = []
    for func_name, func in command_dict.items():
        signature = inspect.signature(func[0])
        parameters = signature.parameters
        param_names = ' '.join(parameters.keys())

        if 'args' in parameters or 'kwargs' in parameters:
            result.append('{:<20s} {:<30s} {:s}'.format(
                func_name, "", func[1]))
        else:
            result.append('{:<20s} {:<30s} {:s}'.format(
                func_name, f"{param_names if param_names else ''}", func[1]))

    headers = '{:<20s} {:<30s} {:s}'.format(
        'Command', 'Parameters', 'Description')
    rows_command = headers + '\n' + '\n'.join(result)

    return rows_command.strip('\n')


# example of parser user_input
def parser_input(user_input: str, command_dict) -> tuple():
    command = None
    arguments = ''

    for key in command_dict.keys():
        if user_input.startswith(key):
            command = key
            arguments = user_input.replace(key, '').strip().split()
            break
    return command, arguments


def main():
    filename = "address_book.txt"
    try:
        load_address_book(filename)
        print("Address book loaded from file.")
    except FileNotFoundError:
        print("New address book created.")
    print("Please input command or start or menu")
    while True:
        print("Please make a choice")
        user_input = input('>>> ').lower()
        # input 'menu' or 'start' to show all funcs
        if user_input == 'menu' or user_input == 'start':
            print("How can I help you?\n")

            print(instruction(command_dict))
        elif user_input in ('good bye', "close", "exit", "0"):
            # del_file_if_empty()
            print('Good bye!')
            break
        else:
            command, arguments = parser_input(user_input, command_dict)
            if command in command_dict:
                result = command_handler(command, command_dict)(*arguments)
            else:
                result = command_handler(user_input, command_dict)
            print(result)


if __name__ == "__main__":
    main()
