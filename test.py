import os
from cfg import Cfg

def process_files_and_folders(base_path, data: dict[list[dict]]):

    named_folders: list[dict] = data.get(Cfg.NAMED_FOLDER)

    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            
            for data_dict in named_folders:
                if dir == data_dict.get(Cfg.SRC):
                    dir = os.path.join(root, dir)

                    for i in os.listdir(dir):

                        img: str = os.path.join(dir, i)

                        if os.path.isfile(img) and img.endswith(Cfg.IMG_EXTS):
                            print(img)



base_path = '/Users/Loshkarev/Desktop/test'

data = {
    Cfg.NAMED_FOLDER: [
        {'src': 'ХО', 'max_size_kb': 100},
        {'src': 'ГО', 'max_size_kb': 50}
    ],
    Cfg.FILE_FOLDER: [
      {'src': '/Users/Loshkarev/Desktop/test/Test 2', 'max_size_kb': 666}, 
        {'src': '/Users/Loshkarev/Desktop/test/Test/file 1.jpg', 'max_size_kb': 123}
    ]
}

process_files_and_folders(base_path, data)
