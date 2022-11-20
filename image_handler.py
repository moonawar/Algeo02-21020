from PIL import Image
import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

# % BAGIAN INI ADALAH HANDLER IMAGE YANG DIGUNAKAN DALAM GUI (TIDAK DIGUNAKAN DALAM ALGORITMA UTAMA) %
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


# % BAGIAN INI ADALAH HANDLER IMAGE YANG DIGUNAKAN DALAM ALGORITMA %
def transformMtoA(matrix):
    #I.S. matrix adalah matriks persegi
    array = np.array([])
    
    for i in range(len(matrix)):
        arraytemp = np.array(matrix[i])
        array = np.concatenate((array, arraytemp))
    return array.astype(int)

def collect_image(size, path = "./dataset"):
    #Try Glob if we also want to store the address
    #Perbaruin biat bisa buka folder dalam folder
    matrix = []
    matrix_name = []
    file_type=[".jpg", ".gif", ".jpeg", ".png"]
    for folder in os.listdir(path):
        if(os.path.splitext(folder)[1] not in file_type):
            folder_path = os.path.join(path,folder)
            print(folder)
            for file in os.listdir(folder_path):  
                if os.path.splitext(file)[1] in file_type:
                    file_path = folder_path + "/" + file
                    img = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
                    #ini method ubahnya bisa diganti mungkin
                    img = cv.resize(img, (size,size))
                    img = transformMtoA(img)
                    matrix.append(img)
                    matrix_name.append(file_path)
                    #matrix_name.append(folder)
        else:
            file_path = path + "/" + folder
            img = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
            #ini method ubahnya bisa diganti mungkin
            img = cv.resize(img, (size,size))
            img = transformMtoA(img)
            matrix.append(img)
            matrix_name.append(folder)   
    return np.array(matrix), matrix_name

# print(transformMtoA([[1,2,3],[4,5,6],[7,8,9]]))

# img_array, img_name = collect_image(256, "./dataset/pins_Henry Cavil")
# print(img_array)