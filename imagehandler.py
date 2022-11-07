from PIL import Image

def SquareCropImage(img):
# Mengembalikan image yang sudah di crop di tengah
    w, h = img.size
    if w > h:
        img = img.crop(((w-h)/2, 0, w-(w-h)/2, h))
    elif h > w:
        img = img.crop((0, (h-w)/2, w, h-(h-w)/2))
    return img

def ResizeImage(img, size):
# Mengembalikan image yang sudah di resize dengan ukuran size x size
    return img.resize((size, size), Image.Resampling.LANCZOS)