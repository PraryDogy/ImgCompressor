import icnsutil

img = icnsutil.IcnsFile()
img.add_media(file='icon.png')
img.write('icon.icns')