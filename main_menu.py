""""This is main Menu"""

from sort import sorter_starter
from addressbook import addressbook_starter # функція адресної книжки заглушка
from notebook import notes_starter #функція записника заглушка

def menu():

    COMMANDS = ["1 - AddressBook", "2 - NoteBook", "3 - Files sorter", "0 - Exit"]
    work_loop = True
    while True:

        print('_'*34 + '\n'+ '|      Welcome to main menu      |\n'+'|'+'_'*32+'|')
        for el in COMMANDS:
            print('|{:<32}|'.format(el))
        print('|'+'_'*32 + '|')
        print('|{:32}|'.format('Type number to start:  '))
        user_input = input("|>>> ")

        if user_input == '1':
            print('\nAddressBook Started!')
            addressbook_starter()
        elif user_input == '2':
            print('\nNoteBook Started!')
            notes_starter()
        elif user_input == '3':
            print('\nFiles Sorter Started!')
            sorter_starter()
        elif user_input == '0':
            work_loop = False
            print('Goodbye!')
            break


if __name__ == '__main__':
    menu()