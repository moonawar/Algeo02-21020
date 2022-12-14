from PIL import Image
import cv2 as cv
import numpy as np
import os

# % BAGIAN INI ADALAH HANDLER IMAGE YANG DIGUNAKAN DALAM GUI (TIDAK DIGUNAKAN DALAM ALGORITMA UTAMA) %
def SquareCropImageTk(img):
# I.S. Image adalah class Image dari library PIL
# F.S. Mengembalikan image yang sudah di crop di tengah

# Gunakan fungsi ini untuk resize image di UI, bukan di algoritma karena class yang dipakai berbeda
    w, h = img.size                                         # Get width and height
    if w > h:                                               # Crop image accordingly based on width and height
        img = img.crop(((w-h)/2, 0, w-(w-h)/2, h))
    elif h > w:
        img = img.crop((0, (h-w)/2, w, h-(h-w)/2))
    return img

def ResizeImage(img, size):
# I.S. Image adalah class Image dari library PIL
# F.S. Mengembalikan image yang sudah di resize dengan ukuran size x size

# Gunakan fungsi ini untuk resize image di UI, bukan di algoritma karena class yang dipakai berbeda
    if not hasattr(Image, 'Resampling'):
        return img.resize((size, size), Image.ANTIALIAS)
    return img.resize((size, size), Image.Resampling.LANCZOS)

# % BAGIAN INI ADALAH HANDLER IMAGE YANG DIGUNAKAN DALAM ALGORITMA %
def SquareCropImageCV(img):
    # I.S. Image adalah matriks persegi
    # F.S. Mengembalikan image yang sudah di crop di tengah
    w, h = img.shape
    if w > h:
        img = img[(w-h)//2:(w-h)//2+h, :]
    elif h > w:
        img = img[:, (h-w)//2:(h-w)//2+w]
    return img


def transformMtoA(matrix):
    #I.S. Matrix adalah matriks persegi
    array = np.array([])

    for i in range(len(matrix)):
        arraytemp = np.array(matrix[i])
        array = np.concatenate((array, arraytemp))

    return array.astype(int)

def transformAtoM(array, size):
    # I.S. Array adalah vektor gambar
    # F.S. Mengembalikan matriks gambar
    matrix = []
    array = array.astype(int)
    for i in range(size):
        matrix.append(array[i * size: (i+1) * size])
    return np.array(matrix)

def collect_image(size, path = "./dataset"):
    # I.S. path adalah path folder yang berisi gambar
    # F.S. Mengembalikan array yang berisi vektor gambar yang sudah di resize

    # OUTPUT ARRAY = N^2 X M, dimana N adalah ukuran gambar, dan M adalah jumlah gambar

    # Try Glob if we also want to store the address
    # Perbaruin biat bisa buka folder dalam folder
    matrix = []
    matrix_name = []
    file_type=[".jpg", ".gif", ".jpeg", ".png"]
    for root, directories, files in os.walk(path):
        for name in files:
            file = os.path.join(root,name)
            if os.path.splitext(name)[1] in file_type:
                img = cv.imread(file, cv.IMREAD_GRAYSCALE)
                img = SquareCropImageCV(img)
                img = cv.resize(img, (size,size))
                img = transformMtoA(img)
                matrix.append(img)
                matrix_name.append(file)
    return np.array(matrix), matrix_name

def get_image(size, image_path):
    # I.S. image_path adalah path image
    # F.S. Mengembalikan array yang berisi vektor gambar yang sudah di resize
    file_type=[".jpg", ".gif", ".jpeg", ".png"]
    if os.path.splitext(image_path)[1] in file_type:
        img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        img = SquareCropImageCV(img)
        img = cv.resize(img, (size,size))
        img = transformMtoA(img)
        return img
    else:
        # This is supposedly can't be reached if input is correct
        return None