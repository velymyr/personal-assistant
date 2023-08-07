from datetime import datetime
from address_book_classes import AddressBook, Name, Phone, Record, Birthday, Email, Address, Note
import re
import pickle


address_book = AddressBook()
filename = 'address_book'


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NameError as e:
            print(
                f"Give me a name and phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except IndexError as e:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except TypeError as e:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except UnboundLocalError as e:
            print("Contact exists")
        except ValueError as e:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except AttributeError as e:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
    return wrapper


@input_error
def add_contact(*args):
    bd = None
    name = Name(args[0])
    list_phones = []
    list_emails = []
    rec: Record = address_book.get(str(name))
    if rec:
        for i in range(1, len(args)):
            print(args[i])
            if not rec.birthday:
                bd = check_bd(args[i])
                if bd:
                    return rec.add_birthday(bd)
            if check_phone(args[i]):
                # if phone:
                list_phones.append(rec.add_phone(args[i]))
                return list_phones
            if check_email(args[i]):
                # if email:
                list_emails.append(rec.add_email(args[i]))
                return list_emails
        # else:
        #     return "Unknown command"
    if not rec:
        for i in range(1, len(args)):
            bd = check_bd(args[i])
            birthday = bd
            if check_phone(args[i]):
                # if phone:
                list_phones.append(args[i])

            if check_email(args[i]):
                list_emails.append(args[i])

        rec = Record(name, phone=list_phones,
                     birthday=birthday, email=list_emails)
        return address_book.add_record(rec)
    else:
        return "Unknown command"


@input_error
def change_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


def check_bd(args):
    pattern_bd = r'(\d\d)/(\d\d)/(\d{4})'
    if re.fullmatch(pattern_bd, args):
        data = Birthday(args)
        if isinstance(data.value, datetime):
            birthday = data
    else:
        birthday = None
    return birthday


def check_email(args):
    pattern = "^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(?:aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])$"
    if re.match (pattern, args):
        email = Email(args)
    print(email)
    return email


def check_phone(args):
    pattern_ph = r"(\+\d{3}\(\d{2}\)\d{3}\-(?:(?:\d{2}\-\d{2})|(?:\d{1}\-\d{3}){1}))"
    if re.fullmatch(pattern_ph, args):
        phone = Phone(args)
    else:
        phone = None
    print(phone)
    return phone

# Видалити запис


@input_error
def delete_record(*args):
    name = Name(args[0])
    if name.value in address_book:
        del address_book[name.value]
        return f"Contact '{name}' has been deleted from the address book."
    return f"No contact '{name}' found in the address book."


# Вийти
def exit_command(*args):
    return "Good bye!"


# коли день народження
@input_error
def get_days_to_birthday(*args):
    name = Name(args[0])
    res: Record = address_book.get(str(name))
    result = res.days_to_birthday(res.birthday)
    if result == 0:
        return f'{name } tomorrow birthday'
    if result == 365:
        return f'{name} today is birthday'
    return f'{name} until the next birthday left {result} days'

# показати контакт


@input_error
def get_phone(*args):
    name = Name(args[0])
    res: Record = address_book.get(str(name))
    result = res.get_phones(res)
    return f"{res.name} : {result}"


# Привіт
def hello(*args):
    return "How can I help you?"

# Невідома команда пуста команда


def no_command(*args, **kwargs):
    return "Unknown command"


# Видалити телефон
@input_error
def remove_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])

    rec: Record = address_book.get(str(name))
    print(rec)
    if rec:
        return rec.remove_phone(phone)
    return f"No contact {name} in address book"


def search_record(*args):
    elem = args[0]
    address_book.save('search')
    fh = open('result', "w")
    with open("search", "r") as file:
        for line in file:
            if not line.find(elem) == -1:
                fh.write(line)
            else:
                continue
    fh.close()
    with open('result', "r") as fh:
        address_book_search = AddressBook()
        # with open( + '.bin', 'rb') as file:
        address_book_search.data = pickle.load(file)
        # for line in fh:
        #     data = line.strip().split(" : ")
        #     name = Name(data[0])
        #     phones = [Phone(phone) for phone in data[1].split(",")]
        #     birthday = Birthday(data[2]) if data[2] else None
        #     emailes = Email(data[3]) if data[3] else None
        #     record = Record(name=name, phone=phones,
        #                     birthday=birthday, email=emailes)
        #     address_book_search.add_record(record)
    return address_book_search

# показати все


@input_error
def show_all_command(*args):
    if Record.__name__:
        return address_book
    # return


# Команди додати, змінити, видалити телефон, вихід, показати все, показати контакт
# COMMANDS = {
#     exit_command: ("good bye", "bye", "exit", "end", "close", "quit", "0"),
#     add_contact: ("add ", "+ ", "1"),
#     change_phone: ("change ", "зміни ", "2"),
#     remove_phone: ("remove ", "delete ", "del ", "-", "3"),
#     show_all_command: ("show all", "show", "4"),
#     get_phone: ("phone ", "5"),
#     get_days_to_birthday: ("birthday", "bd", "6"),
#     delete_record: ("7"),
#     # add_note: ('note', 'нотаток'),
#     search_record: ('search', "find", '8'),
#     hello: ("hello", "hi", "!",)
# }


# def parser(text: str):
#     for cmd, kwds in COMMANDS.items():
#         for kwd in kwds:
#             if text.lower().startswith(kwd):
#                 data = text[len(kwd):].strip().split()
#                 return cmd, data
#     return no_command, []
