from utils import Utils
from PIL import Image

a = '/Users/Loshkarev/Desktop/png/960х412 — копия.png'
# b = Utils.resize_image(a, 300)

# Image.open(a)


img = Image.open(a)
img = img.convert("RGBA")
print(img.getcolors(maxcolors=256*256))