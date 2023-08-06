""""This is main Menu"""

from sort import sorter_starter
from addressbook import addressbook_starter # функція адресної книжки заглушка
from notebook import notes_starter #функція записника заглушка

def menu():

    COMMANDS = ["1️⃣  - AddressBook📒", "2️⃣  - NoteBook📋", "3️⃣  - Files sorter📂", "0️⃣  - Exit❌"]

    while True:

        print("_"*34)
        print("| {:<3} {:^27}|".format("☰","Welcome to main menu"))
        print('|'+'_'*32 + '|')
        for el in COMMANDS:
            print('|{:<33}|'.format(el))
        print('|'+'_'*32 + '|')
        print('|{:<32}|'.format('Type number to start:  '))
        user_input = input("|✍️  " )
        print('|'+'_'*32 + '|')

        if user_input == '1':
            print("_"*34)
            print("|{:^30}|".format("🎉 AddressBook Started! 🎉"))
    
            addressbook_starter()
        elif user_input == '2':
            print("_"*34)
            print("|{:^30}|".format("🎉 NoteBook Started! 🎉"))
    
            notes_starter()
        elif user_input == '3':
            print("_"*34)
            print("|{:^30}|".format("🎉 Files Sorter Started! 🎉"))

            result = sorter_starter()
            print(result)
        elif user_input == '0':
            print('Goodbye!')
            break


if __name__ == '__main__':
    menu()