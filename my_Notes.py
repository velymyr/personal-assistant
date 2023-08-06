import pickle
from collections import UserDict
from rich.console import Console
from rich.table import Table


class Tag:

    def __init__(self, value):
      self.value = value
    
    def __str__(self):
      return self.value

    def __repr__(self):
      return f"{self.value}"

    def __getstate__(self):
      return self.value

    def __setstate__(self, state):
      self.value = state

class Tags:

    def __init__(self):
      self.tags = []

    def __str__(self):
      return ", ".join(str(tag) for tag in self.tags)

    def __repr__(self):
      return f"{self.tags}"

    def __getstate__(self):
      return self.tags

    def __setstate__(self, state):
      self.tags = state

    def __iter__(self):
          return iter(self.tags)
    
  
class Note:

    def __init__(self, note_text):
      self.note_text = note_text

    def __str__(self):
      return self.note_text

    def __repr__(self):
      return f"{self.note_text}"

    def __getstate__(self):
      return self.note_text

    def __setstate__(self, state):
      self.note_text = state


class NoteBook(UserDict):

    def add_note(self, note, tags):
      self.data[note] = tags

    def save(self, filename='notebook_data.pkl'):
      with open(filename, 'wb') as f:
        pickle.dump(self.data, f)

    def load(self, filename='notebook_data.pkl'):
      try:
        with open(filename, 'rb') as f:
          data = pickle.load(f)
          if not isinstance(data, dict):
            raise TypeError('Invalid data type') 
          self.data = data
      except (FileNotFoundError, TypeError):
        self.data = {}

    def show_notes(self):
            n = 1
            console = Console()
            table = Table(show_header=True, header_style="bold magenta", width=60,show_lines=True)
            table.add_column("Number by order", max_width= None)
            table.add_column("Note", width= 20, no_wrap=False)
            table.add_column("Tags")
            
            for key, tags in self.data.items():
                print(key)
                table.add_row(str(n), str(key), ", ".join(str(t) for t in self.data[key]))
                n += 1
            
            console.print(table)

    def change_note(self):
        self.show_notes()
        
        x = input("Choose the note you want to edit by number\n>>> ")
        
        try:
            x = int(x)
            keys = list(self.data.keys())
            if 1 <= x <= len(keys):
                note_to_edit = keys[x - 1]
                new_note = input(f"Enter the new content for note '{note_to_edit}': ")
                new_tags = input(f"Enter the new tags for note '{note_to_edit}' (comma-separated): ").split(",")
                
                self.data[new_note] = [tag.strip() for tag in new_tags]
                if note_to_edit != new_note:
                    del self.data[note_to_edit]
                print(f"Note '{note_to_edit}' has been updated.")
            else:
                print("Invalid input. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def search_note(self, text):
        found_entries = []
        for key, value in self.items():
            if str(key).find(text) != -1:
                found_entries.append((key, value))
        if found_entries:
            print("{:<15} {:<15}".format("Key", "Value"))
            print("=" * 30)
            for entry in found_entries:
                print("{:<15} {:<15}".format(str(entry[0]), str(entry[1])))
        else:
            print("No matching entries found.")

    def search_tag(self, text):
        found_entries = []

        for key, value in self.items():
            tag_lst = ', '.join(str(v) for v in value)
            if text in tag_lst:
                found_entries.append((str(key), tag_lst))

        if found_entries:
            print("{:<15} {:<15}".format("Key", "Tags"))
            print("=" * 30)
            for entry in found_entries:
                print("{:<15} {:<15}".format(entry[0], entry[1]))
        else:
            print("No matching entries found.")

    
nb = NoteBook()

def add_note():

    user_input_note = input('Input your note\n>>>')
    user_input_tags = input('Input tags for a note\n>>>')
    user_input_tags = user_input_tags.strip().split()
    tags = Tags()
    for user_tag in user_input_tags:
        tag = Tag(user_tag)
        
        tags.tags.append(tag)
    note = Note(user_input_note)
    nb.add_note(note, tags)
    return "Note has been added"

def delete_note():
        nb.show_notes()
        
        x = input("Choose the note you want to delete by number\n>>> ")
        
        try:
            x = int(x)
            keys = list(nb.data.keys())
            if 1 <= x <= len(keys):
                note_to_delete = keys[x - 1]
                del nb.data[note_to_delete]
                print(f"Note '{note_to_delete}' has been deleted.")
            else:
                print("Invalid input. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def change_note():
   return nb.change_note()

def exit_notes():
    return "exit"

def show_notes():
    return nb.show_notes()

def search():
    user_choice = input("Enter '1' to search in note\nEnter '2' to search in tags\n>>>")
    search_key = input("Enter a search keyword\n>>>")
    if user_choice == '1':
      return nb.search_note(search_key)
    elif user_choice == '2':
        return nb.search_tag(search_key)
    else:
       return "Wrong input"

note_commands = {
    show_notes: ["show all"],
    exit_notes: ["exit"],
    add_note: ["add"],
    delete_note: ["delete"],
    change_note: ["edit"],
    search: ["search"]
}


def pars(txt_comm: str):
    for key, key_words in note_commands.items():
        for key_word in key_words:
            if txt_comm == key_word:
                return key


def notes_main():
    print("***Hello i`m a notebook.***\nInput:\nadd - to add note\ndelete -to delete note\nedit - to edit note\nsearch - to search note\nshow all - to output all notes\nexit - to exit")
    nb.load()
    while True:
        user_input_command = str(input("Input a command\n>>>"))
        command = pars(user_input_command.lower())
        if command is None:
            print('Wrong command')
        elif command == exit_notes:
            nb.save()
            print('Notebook closed')
            break
        else:
            result = command()
            nb.save()
            if result:
                print(result)


if __name__ == "__main__":
    notes_main()