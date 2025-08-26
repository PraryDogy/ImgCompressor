import os
import json

class Cfg:
    app_name = "ImgCompressor"
    app_ver = "1.1.0"

    NAMED_FOLDERS = "named_folders"
    OTHERS = "___others___"
    SPECIFIC_FOLDERS = "specific_folders"

    FLAG = "flag"
    SRC = "src"
    MAX_SIZE_KB = "max_size_kb"

    IMG_EXTS = ('.jpg', '.jpeg', '.png')

    ignore_png = False
    app_support = os.path.expanduser(f"~/Library/Application Support/{app_name}")
    json_file = os.path.join(app_support, "cfg.json")

    @classmethod
    def init(cls):
        os.makedirs(cls.app_support, exist_ok=True)
        if not os.path.exists(cls.json_file):
            cls.write_json()
        else:
            with open(cls.json_file, "r", encoding="utf-8") as file:
                data: dict = json.load(file)
                for k, v in data.items():
                    if hasattr(cls, k):
                        setattr(cls, k, v)

    @classmethod
    def write_json(cls):
        with open(cls.json_file, "w", encoding="utf-8") as file:
            data = {
                "ignore_png": cls.ignore_png,
            }
            json.dump(data, file, indent=4, ensure_ascii=False)
