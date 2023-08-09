from datetime import datetime
from address_book_classes import AddressBook, Name, Phone, Record, Birthday, Email, Address, Note
import re

address_book = AddressBook()
filename = 'address_book'


def input_error(func):
    def wrapper(*args, **kwargs):
        error_mgs = 'Give me correct parameters command+name--> enter'
        try:
            return func(*args, **kwargs)
        except UnboundLocalError as e:
            print("Contact exists")
        except NameError as e:
            print(error_mgs)
        except IndexError as e:
            print(error_mgs)
        except TypeError as e:
            print(error_mgs)
        except ValueError as e:
            print(error_mgs)
        except AttributeError as e:
            print(error_mgs)

    return wrapper




@input_error
def change_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


# def check_bd(args):
#     pattern_bd = r'(\d\d)/(\d\d)/(\d{4})'
#     if re.fullmatch(pattern_bd, args):
#         data = Birthday(args)
#         if isinstance(data.value, datetime):
#             birthday = data
#     else:
#         birthday = None
#     return birthday


# def check_email(args):
#     pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
#     if re.match(pattern, args):
#         email = Email(args)
#     print(email)
#     return email


# def check_phone(args):
#     pattern_ph = r"(\+\d{3}\(\d{2}\)\d{3}\-(?:(?:\d{2}\-\d{2})|(?:\d{1}\-\d{3}){1}))"
#     if re.fullmatch(pattern_ph, args):
#         phone = Phone(args)
#     else:
#         phone = None
#     print(phone)
#     return phone



@input_error
def edit(name, parameter, new_value):
    res: Record = address_book.get(str(name))
    #print(res)
    try:
        if res:
            if parameter == 'birthday':
                new_value = Birthday(new_value).value
            elif parameter == 'email':
                parameter= 'emailes'
                new_contact = new_value.split(' ')
                new_value = []
                for emailes in new_contact:
                        new_value.append(Email(emailes).value)
            elif parameter == 'address':
                new_value = Address(new_value).value
            elif parameter == 'note':
                new_value = Note(new_value).value
            elif parameter == 'phones':
                new_contact = new_value.split(' ')
                new_value = []
                for number in new_contact:
                        new_value.append(Phone(number).value)
            if parameter in res.__dict__.keys():
                res.__dict__[parameter] = new_value
        res: Record = address_book.get(str(name))
        print(res)   
    except ValueError:
        print('Incorrect parameter! Please provide correct parameter')
    except NameError:
        print('There is no such contact in address book!')
    


# Видалити запис
@input_error
def delete_record(*args):
    name = Name(args[0])
    if name.value in address_book:
        del address_book[name.value]
        return f"Contact '{name}' has been deleted from the address book."
    return f"No contact '{name}' found in the address book."


# # Вийти
# def exit_command(*args):
#     return "Good bye!"


# коли день народження
# @input_error
# def get_days_to_birthday(*args):
#     name = Name(args[0])
#     res: Record = address_book.get(str(name))
#     result = res.days_to_birthday(res.birthday)
#     if result == 0:
#         return f'{name } tomorrow birthday'
#     if result == 365:
#         return f'{name} today is birthday'
#     return f'{name} until the next birthday left {result} days'

# показати контакт
@input_error
def get_phone(*args):
    name = Name(args[0])
    res: Record = address_book.get(str(name))
    result = res.get_phones(res)
    return f"{res.name} : {result}"


# # Привіт
# def hello(*args):
#     return "How can I help you?"

# # Невідома команда пуста команда


# def no_command(*args, **kwargs):
#     return "Unknown command"


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


