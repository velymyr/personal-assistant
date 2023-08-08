from datetime import datetime
from address_book import AddressBook, Name, Phone, Record, Birthday, Email, Address, Note
import re
# import pickle


address_book = AddressBook()
filename = 'address_book'


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NameError:
            print(
                f"Give me a name and phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except IndexError:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except TypeError:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except UnboundLocalError:
            print("Contact exists")
        except ValueError:
            print(
                f"Give me a name and  phone number in format +380(88)777-77-77 or date birthday dd/mm/YYYY")
        except AttributeError:
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


@input_error
def get_phone(*args):
    name = Name(args[0])
    res: Record = address_book.get(str(name))
    result = res.get_phones(res)
    return f"{res.name} : {result}"
