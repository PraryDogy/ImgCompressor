

# Функция находит внутри Downloads
# Все папки с именем ГО и выводит 100
# Все папки с именем ХО и выводит 200
# Папку Test и выводит 300
# Папку Test 2 и выводит 400
# Файл file.jpg и выводит 500
# Файл file 2.jpg и выводит 500
# Остальные файлы и папки в Downloads не трогает



import os

def find_and_print_sizes(src, named_folders, single_folders, single_files):
    for root, dirs, files in os.walk(src):
        # Проверяем папки по имени
        for folder in dirs:
            for named in named_folders:
                if folder == named["folder_name"]:
                    print(named["size"])
                    break
        
        # Проверяем папки по пути
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            for single in single_folders:
                if folder_path == single["folder_name"]:
                    print(single["size"])
                    break

        # Проверяем файлы
        for file in files:
            file_path = os.path.join(root, file)
            for single in single_files:
                if file_path == single["folder_name"]:
                    print(single["size"])
                    break


src = "/Users/Loshkarev/Desktop/test"


"folder_name", "size"


named_folders = [
    {"folder_name": "ГО", "size": 100},
    {"folder_name": "ХО", "size": 200}
]

single_folders = [
    {"folder_name": "/Users/Loshkarev/Desktop/test/Test 2", "size": 300},
    {"folder_name": "/Users/Loshkarev/Desktop/test/Test", "size": 400}
]

single_files = [
    {"folder_name": src + "/file.jpg", "size": 500},
    {"folder_name": src + "/file_2.jpg", "size": 600}
]


find_and_print_sizes(src, named_folders, single_files, single_files)