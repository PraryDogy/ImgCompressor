from utils import Utils
from PIL import Image
import os

a = '/Volumes/Macintosh HD/Users/Loshkarev/Desktop/png/1472 х 600.png'
b = Utils.resize_image(a, 300)
size = int(os.path.getsize(a) / 1024)
print(size, "kb")