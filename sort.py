import os
import shutil
from pathlib import Path
from normalize import normalize


CATEGORIES = {"Audio": [".mp3", ".aiff", ".wav", ".ogg"],
              "Video": [".mkv", ".mov", ".mp4", ".avi"],
              "Document": [".docx", ".pptx", ".doc", ".txt", ".pdf", ".xlsx", ".pptx", ".rtf", ".xls", ".pub"],
              "Image": [".jpeg", ".png", ".svg", ".jpg", ".bmp", ".gif"],
              "Archive": [".zip", ".tar", ".7z", ".gz"],
              "Python": [".py", ".json", ".pyc"],
              "Other": [] }
dict_of_files = {}
dict_global = {}
dict_of_ext = {}
dict_ext = {}


def move_file(path: Path, root_dir: Path,  categories: str):
    target_dir = root_dir.joinpath(categories)
    if not target_dir.exists():
        target_dir.mkdir()
    
    path.replace(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))


def unpack_archive(path: Path):
    archive_folder = "Archive"
    ext = [".zip", ".tar", ".7z", ".gz", ".rar"]

    for el in path.glob(f"**/*"):  # Обираю цей варіант суто для розширення охоплення пошуку, якщо наприклад якийсь архів не було відсортовано в папку Архів. Логічно що ми передаємо такі само розширення в функцію, але наприклад тут вже можна додати більше розширень задля охоплення більше файлів.
        if not el.name.startswith('.'):
            if el.suffix in ext:
                filename = el.stem
                arch_dir = path.joinpath(path/archive_folder/filename)
                arch_dir.mkdir()
                try:
                    shutil.unpack_archive(el, arch_dir)
                except shutil.ReadError:
                    print("| {:^74} |".format('This file format is not suported:'))
                    print("|- {:<74}|".format(el.name))
                    print('|____________________________________________________________________________|')

            else:
                continue


def delete_empty_folder(path: Path):

    folders_to_delete = [f for f in path.glob("**")]
    for folder in folders_to_delete[::-1]:
        if not folder.name.startswith('.'):
            try:
                folder.rmdir()
            except OSError:
                continue


def get_categories(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Unknown extension"


def sort_folder(path: Path):
    for item in path.glob("**/*"):
        if not item.name.startswith('.'):
            if item.is_file():
                cat = get_categories(item)
                move_file(item, path, cat)


def files_sorter(path: Path):  
    for item in path.glob("**/*"):
        if not item.name.startswith('.'):
            if item.is_file():
                # print(item)
                cat = get_categories(item)
                if dict_of_files.get(cat):
                    dict_of_files[cat].append(item.name)
                else:
                    dict_of_files[cat] = [item.name]
    dict_global.update(dict_of_files)
    print(' ____________________________________________________________________________')
    print("| {:^74} |".format("▣ Files found in folders: ▣"))
    print('|____________________________________________________________________________|')
    for el, values in dict_global.items():
        print('|____________________________________________________________________________|')
        print("| {:^74} |".format(str("▣ "+ el + " ▣")))
        print('|____________________________________________________________________________|')
        for value in values:
            print("| {:<74} |".format(str(("► "+ value))))
    print('|____________________________________________________________________________|')
    


def files_ext(path: Path):
    for item in path.glob('**/*'):
        if not item.name.startswith('.'):
            if item.is_file():
                cat = get_categories(item)
                if dict_of_ext.get(cat):
                    dict_of_ext[cat].add(item.suffix)
                else:
                    dict_of_ext[cat] = {item.suffix}

    dict_ext.update(dict_of_ext)

    print('\n ____________________________________________________________________________')
    print("| {:^74} |".format("▣ Extensions found in files: ▣"))
    print('|____________________________________________________________________________|')
    for el, val in dict_ext.items():
        print("| {:<20} | {:<51} |".format(str("▶ "+el), str(", ".join(val))))
    print('|____________________________________________________________________________|')


def sorter_starter():

    print("|{:^32}|".format("▣ For exit type 'exit' or '0' ▣"))
    print("|"+"_"*32 + "|")
    print("|{:^32}|".format("Input path to folder:"))
    print("|"+"_"*32 + "|")

    while True:

        try:
            # do not forget to change path lib sys.argv[1]
            path = Path(input("|>>> "))
            if path.name.lower() in ("close", "exit", "good bye", "0"):
                return "\nGood bye!"
            elif path.exists():
                print("|"+"_"*32 + "|"+"\n")
                print("_"*78)
                print("|{:^70}|".format("✨✨✨ Sorting completed! ✨✨✨"))
                print("|"+"_"*76 + "|")   
            else:
                print("_"*34)
                print("|{:<32}|".format("Folder with this path not exist"))
                print("|{:<32}|".format("Try again..."))
                print("|"+"_"*32 + "|"+"\n")
                continue 
            
        except IndexError:
            return "\n"
           
        
        sort_folder(path)
        delete_empty_folder(path)
        unpack_archive(path)
        files_sorter(path)
        files_ext(path)

        print("\nIf you like to continue type 'resume' or type 'exit' to exit\n")
        user_answer = input("|>>> ")
        if user_answer.lower() in ("close", "exit", "goodbye", "0"):
            return '\nGood bye!'
        else:
            print("\nInput path to folder:\n")
            continue
        
        
if __name__ == "__main__":
    sorter_starter()
