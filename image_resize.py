import cv2 as cv
import numpy as np
import os



def transformMtoA(matrix):
    #I.S. matrix adalah matriks persegi
    array =np.array([])
    for i in range(len(matrix)):
        arraytemp = np.array(matrix[i])
        np.concatenate((array, arraytemp))
    return array




def collect_image(size, path = "./dataset"):
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
                    file_path = folder_path+"/"+file
                    img = cv.imread(file_path, 0)
                    #ini method ubahnya bisa diganti mungkin
                    img = cv.resize(img, (size,size))
                    img = transformMtoA(img)
                    matrix.append(img)
                    matrix_name.append(folder)
        else:
            file_path = path+"/"+folder
            img = cv.imread(file_path, 0)
            #ini method ubahnya bisa diganti mungkin
            img = cv.resize(img, (size,size))
            img = transformMtoA(img)
            matrix.append(img)
            matrix_name.append(folder)   
    return matrix, matrix_name

img_array, img_name = collect_image( 256,"./dataset")
print(img_array)




