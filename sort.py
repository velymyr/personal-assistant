import sys
import shutil
from pathlib import Path
from normalize import normalize


CATEGORIES = {"Audio": [".mp3", ".aiff", ".wav", ".ogg"],
              "Video": [".mkv", ".mov", ".mp4", ".avi"],
              "Document": [".docx", ".pptx", ".doc", ".txt", ".pdf", ".xlsx", ".pptx", ".rtf", ".xls", ".pub"],
              "Image": [".jpeg", ".png", ".svg", ".jpg", ".bmp"],
              "Archive": [".zip", ".tar", ".rar", ".7z", ".gz"],
              "Python": [".py", ".json", ".pyc"],
              "Unknown extension": [], }
dict_of_files = {}
dict = {}
dict_of_ext = {}
dict_ext = {}


def move_file(path: Path, root_dir: Path,  categories: str):
    target_dir = root_dir.joinpath(categories)
    if not target_dir.exists():
        print(f"Make {target_dir}")
        target_dir.mkdir()
    
    path.replace(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))


def unpack_archive(path: Path):
    archive_folder = "Archive"
    ext = [".zip", ".tar"]

    for el in path.glob(f"**/*"):  # Обираю цей варіант суто для розширення охоплення пошуку, якщо наприклад якийсь архів не було відсортовано в папку Архів. Логічно що ми передаємо такі само розширення в функцію, але наприклад тут вже можна додати більше розширень задля охоплення більше файлів.
        if el.suffix in ext:
            filename = el.stem
            arch_dir = path.joinpath(path/archive_folder/filename)
            arch_dir.mkdir()
            shutil.unpack_archive(el, arch_dir)
        else:
            continue


def delete_empty_folder(path: Path):

    folders_to_delete = [f for f in path.glob("**")]
    for folder in folders_to_delete[::-1]:
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
      
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def files_sorter(path: Path):  
    for item in path.glob("**/*"):
        if item.is_file():
            # print(item)
            cat = get_categories(item)
            if dict_of_files.get(cat):
                dict_of_files[cat].append(item.name)
            else:
                dict_of_files[cat] = [item.name]
    dict.update(dict_of_files)
    print('\n ____________________________________________________________________________')
    print("| {:^72} |".format("👇 Files found in folders: 👇"))
    print('|____________________________________________________________________________|')
    for el, values in dict.items():
        print('|____________________________________________________________________________|')
        print("| {:^73} |".format(str("👉 "+ el)))
        print('|____________________________________________________________________________|')
        for value in values:
            print("| {:<73} |".format(str(("➖ "+ value))))
    print('|____________________________________________________________________________|')
    


def files_ext(path: Path):
    for item in path.glob('**/*'):
        if item.is_file():
            cat = get_categories(item)
            if dict_of_ext.get(cat):
                dict_of_ext[cat].add(item.suffix)
            else:
                dict_of_ext[cat] = {item.suffix}

    dict_ext.update(dict_of_ext)

    print('\n ____________________________________________________________________________')
    print("| {:^74} |".format("Extensions found in files:"))
    print('|____________________________________________________________________________|')
    for el, val in dict_ext.items():
        print("| {:<20} | {:<51} |".format(str(el), str(", ".join(val))))
    print('|____________________________________________________________________________|')


def sorter_starter():

    print("|"+"_"*32 + "|")
    print("|{:^32}|".format("Input path to folder:"))
    print("|"+"_"*32 + "|")

    while True:
        try:
            # do not forget to change path lib sys.argv[1]
            path = Path(input("|✍️  "))
            print("|"+"_"*32 + "|")
            print("_"*34)
            print("|{:^24}|".format("🎉🎉🎉 Sorting completed! 🎉🎉🎉"))
            print("|"+"_"*32 + "|") 
            
        except IndexError:
            return "\n"

        if path.name.lower() in ("close", "exit", "good bye"):
            return "\nGood bye!"
        elif not path.exists():
            print("_"*34)
            print("|{:<32}|".format("Folder with this path not exist"))
            print("|{:<32}|".format("Try again..."))
            print("|"+"_"*32 + "|"+"\n")
            continue

            
        
        sort_folder(path)
        delete_empty_folder(path)
        unpack_archive(path)
        files_sorter(path)
        files_ext(path)

        print("\nIf you like to continue type 'resume' or type 'close' to exit\n")
        user_answer = input("|✍️  ")
        if user_answer.lower() in ("close", "exit", "goodbye"):
            return '\nGood bye!'
        else:
            print("\nInput path to folder:\n")
            continue
        
        
if __name__ == "__main__":
    sorter_starter()
