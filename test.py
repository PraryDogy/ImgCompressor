import os

# Функция находит внутри Downloads
# Все папки с именем ГО и выводит 100
# Все папки с именем ХО и выводит 200
# Папку Test и выводит 300
# Папку Test 2 и выводит 400
# Файл file.jpg и выводит 500
# Файл file 2.jpg и выводит 500
# Остальные файлы и папки в Downloads не трогает


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
    {"folder_name": "/Users/Loshkarev/Desktop/test/single files/file 2.jpg", "size": 500},
    {"folder_name": "/Users/Loshkarev/Desktop/test/file 1.jpg", "size": 600}
]

for root, dirs, files in os.walk(src):

    for dir in dirs:
        
        for data in named_folders:
            if dir == data.get("folder_name"):
                print(os.path.join(root, dir))
                ...

    for dir in dirs:

        src_ = os.path.join(root, dir)

        for data in single_folders:

            if src_ == data.get("folder_name"):
                print(src_)
                ...

    for file in files:

        src = os.path.join(root, file)

        for data in single_files:

            if src == data.get("folder_name"):

                print(src)
                ...