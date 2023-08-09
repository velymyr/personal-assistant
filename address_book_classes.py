from collections import UserDict
from bd import main_bd
import re
from datetime import datetime as dt
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table
import csv
import json
import pickle
import os


class Field:

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):

    def __init__(self, value):
        while True:
            self.value = value
            if self.value:
                self.values = value
                break
            else:
                print('Incorrect name')
                value = input("Name: ")

            # try:
            # #     for number in self.values.split(' '):
            # #         if re.match('^\+\d{12}$', number) or number == '':
            # #             self.value.append(number)
            # #         else:
            # #             raise ValueError
            # except ValueError:

            # else:


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
                if re.match ("^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(?:aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])$", self.value) or self.value == '':
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

    def serialize_to_csv(self):
        filename='address_book.csv'
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            print(self.data)
            for rec in self.data.values():
                print(rec)
                name = rec.name
                phones = [phone for phone in rec.phones]
                birthday = rec.birthday.strftime(
                    "%d/%m/%Y") if rec.birthday else ""
                emailes = [email for email in rec.emailes]
                address = rec.address
                note = rec.note
                writer.writerow(
                    [name, ",".join(phones), birthday, ",".join(emailes), address, note])
        return "csv"

    # def serialize_to_pickle(self, filename):
    #     with open(filename, "wb") as fh:
    #         pickle.dump(self.data, fh)

    def serialize_to_json(self):
        filename='address_book.json'
        data_list = []
        for record in self.data.values():
            data = {
                "name": record.name,
                "phones": [phone for phone in record.phones],
                "birthday": record.birthday.strftime("%d/%m/%Y") if record.birthday else "",
                "emailes": [email for email in record.emailes],
                "address": record.address,
                "note": record.note
            }
            data_list.append(data)
        with open(filename, "w") as file:
            json.dump(data_list, file)

    def save(self):
        with open('address_book.bin', 'wb') as file:
            pickle.dump(self.data, file)
        return 'OK'

    def load(self, file_name):
        #emptyness = os.stat(file_name + '.bin')
        with open(file_name, 'rb') as file:
            self.data = pickle.load(file)
        return self.data

    def get_current_week(self):
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]


    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {'Monday': [], 'Tuesday': [],
                        'Wednesday': [], 'Thursday': [], 'Friday': []}
        for rec in self.data.values():
            #print(rec.birthday)
            if rec.birthday is not None:
                new_birthday = rec.birthday.replace(year=current_year)
                #print(new_birthday)
                birthday_weekday = new_birthday.weekday()
                if self.get_current_week()[0] <= new_birthday < self.get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(rec.name)
                    else:
                        congratulate['Monday'].append(rec.name)
        for key, value in congratulate.items():
            if len(value):
                result.append(f"Don't forget to Say Happy Birthday in {key} to {' '.join(value)}")
        return '_' * 60 + '\n' + '\n'.join(result) + '\n' + '_' * 60
    

    

    def who_has_birthday_after_n_days(self, n_days):      
        current_date = dt.now()
        current_year = dt.now().year
        future_birthday = current_date + timedelta(days=n_days)
        #print (future_birthday.date())
        contacts_with_birthday = []

        for rec in self.data.values():
            #print (rec)
            if rec.birthday is not None:
                new_year= date(current_year,12,31)
                #print(new_year)
                remaining_days_in_year = new_year - future_birthday.date()
                #print (remaining_days_in_year.days)
                if remaining_days_in_year.days > n_days:
                    birthday_this_year = rec.birthday.replace(year=current_year)
                    #print (birthday_this_year)
                    if future_birthday.date() == birthday_this_year:
                        contacts_with_birthday.append(rec.name)
                else: 
                    birthday_next_year = rec.birthday.replace(year=(current_year + 1))
                    if future_birthday.date() == birthday_next_year:
                        contacts_with_birthday.append(rec.name)

        if contacts_with_birthday:
            return ', '.join(name for name in contacts_with_birthday)
        else:
            return f"Nobody has birthday after {n_days} days"

    def show_all_address_book(self):
            console = Console()
            table = Table(show_header=True, header_style="bold magenta", width=120,show_lines=True)
            table.add_column("Name", width= 40, no_wrap=False)
            table.add_column("Phones", width= 40, no_wrap=False)
            table.add_column("Birthday", width= 40, no_wrap=False)
            table.add_column("Emails", width= 40, no_wrap=False)
            table.add_column("Address", width= 40, no_wrap=False)
            table.add_column("Note", width= 40, no_wrap=False)
            
            for record in self.data.values():
                name = record.name
                phones = ", ".join(str(phone) for phone in record.phones)
                bday = str(record.birthday) if record.birthday else ""
                emails = ", ".join(str(email) for email in record.emailes)
                address = str(record.address) if record.address else ""
                note = str(record.note) if record.note else ""
                
                table.add_row(name, phones, bday, emails, address, note)
            
            console.print(table)
    def show_all_address_book(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta",
                      width=120, show_lines=True)
        table.add_column("Name", width=40, no_wrap=False)
        table.add_column("Phones", width=40, no_wrap=False)
        table.add_column("Birthday", width=40, no_wrap=False)
        table.add_column("Emails", width=40, no_wrap=False)
        table.add_column("Address", width=40, no_wrap=False)
        table.add_column("Note", width=40, no_wrap=False)

        for record in self.data.values():
            name = record.name
            phones = ", ".join(str(phone) for phone in record.phones)
            bday = str(record.birthday) if record.birthday else ""
            emails = ", ".join(str(email) for email in record.emailes)
            address = str(record.address) if record.address else ""
            note = str(record.note) if record.note else ""

            table.add_row(name, phones, bday, emails, address, note)

        console.print(table)
        return "Success!\n"
    
    def search(self, string: str):
        output = ''
        for key in self.keys():
            rec = self[key]
            phone = '.'.join(phone for phone in rec.phones)

            if rec.birthday == "":
                show_birthday = ""
            else:
                show_birthday = datetime.strftime(rec.birthday, '%d/%m/%Y')

            emailes = ".".join(email for email in rec.emailes)
            address = rec.address
            note = rec.note

            if string in str(rec.name.lower()) or string in phone or string in show_birthday or string in emailes or string in address or string in note:
                output += str(rec)
        return output
