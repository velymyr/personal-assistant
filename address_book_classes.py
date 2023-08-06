from collections import UserDict
from bd import main_bd
import re
from datetime import datetime as dt
import csv
import json
import pickle


class Field:

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value=''):
        while True:
            self.value = []
            if value:
                self.values = value
            else:
                self.values = input(
                    "Phones(+12digits) (Введіть номер телефона + і дванадцять цифр): ")
            try:
                for number in self.values.split(','):
                    if re.match('^\+\d{12}$', number) or number == '':
                        result = '{}({}){}-{}-{}'.format(number[0:3], number[4:5],
                                                         number[6:8], number[9:10], number[11:12])
                        # result = f"{number[0]}{number[1]}{number[2]}{number[3]}({number[4]}{number[5]}){number[6]}{number[7]}{number[8]}-{number[9]}{number[10]}-{number[11]}{number[12]}"
                        self.value.append(result)
                    else:
                        raise ValueError
            except ValueError:
                print(
                    'Incorrect phone number format! Please provide correct phone number format.')
            else:
                break

    def __getitem__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = value

        except ValueError:
            return

    def __str__(self):
        return self.__value


class BirthdayError(Exception):
    ...


class Birthday(Field):
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Birthday date(dd/mm/YYYY): ")
            try:
                if re.match('^\d{2}/\d{2}/\d{4}$', self.value):
                    self.value = dt.strptime(self.value.strip(), "%d/%m/%Y")
                    break
                elif self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect date! Please provide correct date format.')

    def __getitem__(self):
        return self.value
    #     return self.__value.strftime("%d/%m/%Y")


class Email(Field):
    def __init__(self, value=''):
        while True:

            if value:
                self.value = value
            else:
                self.value = input("Email: ")
            try:
                regex = re.compile(
                    r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
                if (regex, self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect email! Please provide correct email.')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = value

        except ValueError:
            return

    def __str__(self):
        return self.__value


class Address(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value


class Note(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None, address: Address = None, note: Note = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.emailes = []
        self.address = address
        self.note = note
        if email:
            if isinstance(email, list):
                self.emailes.extend(email)
            else:
                self.emailes.append(email)
        if phone:
            if isinstance(phone, list):
                self.phones.extend(phone)
            else:
                self.phones.append(phone)

    def add_birthday(self, birthday: Birthday):
        if not self.birthday:
            self.birthday = birthday
            return f"birthday {self.birthday} add to contact {self.name}"
        return f"{self.birthday} allready present in birthday data of contact {self.name}"

    def add_phone(self, phone: Phone):
        if phone.value.strip() not in [p.value.strip() for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def add_email(self, email: Email):
        if email.value in [e.value for e in self.emails]:
            return f"{email} present in emails of contact {self.name}"
        self.emails.append(email)
        return f"email {email} add to contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"

    def days_to_birthday(self, birthday: Birthday):
        result = main_bd(birthday)
        return result

    def get_phones(self, res):
        result = f"{', '.join(str(p) for p in res.phones)}"
        return result

    def __str__(self) -> str:
        return f"{self.name} : {', '.join(p for p in self.phones)}  {(str(self.birthday))} {', '.join(p for p in self.emailes)} {(str(self.address))} {(str(self.note))} "

    def remove_phone(self, phone):
        for idx, p in enumerate(self.phones):
            print(len(p.value))
            print(len(phone.value))
            if phone.value.strip() == p.value.strip():
                old_phone = (self.phones[idx])
                self.phones.remove(self.phones[idx])
                return f"The phone {old_phone} is deleted"
        return f"{phone} not present in phones of contact {self.name}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        # add to file
        return f"Contact {record} add success"

    def __str__(self):  # -> str:
        return "\n".join(str(r) for r in self.data.values())

    def iterator(self, n=3):
        result = []
        counter = 0
        for record in self.data.values():
            result.append(str(record))
            counter += 1
            if counter >= n:
                yield "\n".join(result)
                counter = 0
                result = []
        if result:
            yield "\n".join(result)

    def serialize_to_csv(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            print(self.data)
            for rec in self.data.values():
                print(rec)
                name = rec.name.value
                phones = [phone.value for phone in rec.phones]
                birthday = rec.birthday.value.strftime(
                    "%d/%m/%Y") if rec.birthday else ""
                emailes = [email.value for email in rec.emailes]
                writer.writerow(
                    [name, ",".join(phones), birthday, ",".join(emailes)])
            # writer.writerow(self.data.values())

    def serialize_to_pickle(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.data, fh)

    def serialize_to_json(self, filename):
        data_list = []
        for record in self.data.values():
            data = {
                "name": record.name.value,
                "phones": [phone.value for phone in record.phones],
                "birthday": record.birthday.value.strftime("%d/%m/%Y") if record.birthday else "",
            }
            data_list.append(data)

        with open(filename, "w") as file:
            json.dump(data_list, file)
