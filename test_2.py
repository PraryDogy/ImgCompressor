# from utils import Utils
# from PIL import Image
# import os

# a = '/Volumes/Macintosh HD/Users/Loshkarev/Desktop/png/1472 х 600.png'
# # b = Utils.resize_image(a, 300)


# from PIL import Image
# import numpy as np
# img = Image.open(a).convert("RGB")
# img_arr = np.array(img, dtype=np.uint8)
# img_arr = ((img_arr >> 3) << 3).astype('uint8')
# img_reduced = Image.fromarray(img_arr, "RGB")
# img_8bit = img_reduced.convert("P", palette=Image.ADAPTIVE, colors=256)
# img_8bit.save("output.png", optimize=True)

# print(os.path.getsize("output.png") / 1024)

tet = [1, 2, 3, 4, 5]

a = tet[-3:]

print(a)