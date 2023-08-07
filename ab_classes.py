from collections import UserDict
from bd import main_bd
import re
from datetime import datetime as dt
# import csv
# import json
import pickle
# filename= 'address_book_1.txt'


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
                for number in self.values.split(' '):
                    if re.match('^\+\d{12}$', number) or number == '':
                        self.value.append(number)
                    else:
                        raise ValueError
            except ValueError:
                print(
                    'Incorrect phone number format! Please provide correct phone number')
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
                    self.value = self.value.date()
                    break
                elif self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect date! Please provide correct date format.')

    def __getitem__(self):
        return self.value.date()


class Email(Field):
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Email: ")
            try:
                if re.match ("^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+/=?^_`{|}\
                ~]+)*@(?:[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(?:aero|arpa|asia|biz|cat|\
                com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|\
                travel|[a-z][a-z])$", self.value) or self.value == '':
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

    def __init__(self, name: Name, phone: Phone = None,
                 birthday: Birthday = None, email: Email = None,
                 address: Address = None, note: Note = None) -> None:
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
            print(f'p= {self.phones[idx]}')
            if phone == p:
                old_phone = (self.phones[idx])
                self.phones.remove(self.phones[idx])
                return f"The phone {old_phone} is deleted"
        return f"{phone} not present in phones of contact {self.name}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
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

    # def serialize_to_csv(self, filename):
    #     with open(filename, "w", newline="") as file:
    #         writer = csv.writer(file)
    #         print(self.data)
    #         for rec in self.data.values():
    #             print(rec)
    #             name = rec.name.value
    #             phones = [phone.value for phone in rec.phones]
    #             birthday = rec.birthday.value.strftime(
    #                 "%d/%m/%Y") if rec.birthday else ""
    #             emailes = [email.value for email in rec.emailes]
    #             writer.writerow(
    #                 [name, ",".join(phones), birthday, ",".join(emailes)])

    # def serialize_to_pickle(self, filename):
    #     with open(filename, "wb") as fh:
    #         pickle.dump(self.data, fh)

    # def serialize_to_json(self, filename):
    #     data_list = []
    #     for record in self.data.values():
    #         data = {
    #             "name": record.name.value,
    #             "phones": [phone.value for phone in record.phones],
    #             "birthday": record.birthday.value.strftime("%d/%m/%Y") if record.birthday else "",
    #         }
    #         data_list.append(data)
    #     with open(filename, "w") as file:
    #         json.dump(data_list, file)

    # def save(self, file_name):
    #     with open(file_name + '.bin', 'wb') as file:
    #         pickle.dump(self.data, file)
    #     return 'OK'

    def load(self, file_name):
        with open(file_name + '.bin', 'rb') as file:
            self.data = pickle.load(file)
        return self.data

    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {'Monday': [], 'Tuesday': [],
                        'Wednesday': [], 'Thursday': [], 'Friday': []}
        for account in self.data:
            print(account)
            if account[self.birthday]:
                new_birthday = account[self.birthday].replace(
                    year=current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday.date() < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(
                            account['name'])
                    else:
                        congratulate['Monday'].append(account['name'])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return '_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50