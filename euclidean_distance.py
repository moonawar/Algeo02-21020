import numpy as np

def euclidean_distance(v1,v2):
    #I.S. len(v1) = len(v2), v1 v2 array linear
    # Mengembalikan euclidean_distance dari v1 v2 (float)
    result = 0
    for i in range(len(v1)):
        result += (v1[i]-v2[i])^2
    result /= (result)**0.5
    return result



def sum2Array(array1, array2):
    #Syarat
    #len(array1)==len(array2)
    array3 = []
    for i in range(len(array1)):
        array3.append(array1[i]+array2[i])
    return array3




def arrayMeanInt(array_of_image):
    #I.S. Array yang berisi vektor gambar
    #Rata - Rata yang dihasilkan di floor
    array_of_imageO = array_of_image[0]
    count = 1
    for i in range(1,len(array_of_image)):
        array_of_imageO = sum2Array(array_of_imageO, array_of_image[i])
        count +=1
    for i in range(len(array_of_imageO)):
        array_of_imageO[i]//=count
    return array_of_imageO





def subtractArray(array1, array2):
    array = []
    for i in range(len(array1)):
        array.append(array1[i]-array2[i])
    return array

def findMinDistance(array, val):
    # Mengembalikan index yang euclidean distancenya paling kecil dengan val
    min = euclidean_distance(val, array[0])
    index = 0
    for i in range(len(array)):
        temp = euclidean_distance(array[i], val)
        if min>temp:
            min = temp
            index = i
        else:
            continue
    return index


def getEigenface(array_of_images,eigenVector):
    #Cuman 1 eigenface
    #Berdasarkan docs e eigenface = eigen_vector*mean_diff
    # yang dipake crossproduct of normalized array of images and eigenVector
    #
    eigenFaces = np.matmul(array_of_images, eigenVector)
    for i in range(len(array_of_images)):
        eigen_face = get_column(eigenFaces,i)
    return eigen_face





def get_column(array_of_images, index):
    vectors = []
    for i in range(array_of_images.shape[0]):
        vectors.append(array_of_images[i][0])
    return vectors

def calculateOmega(image, eigenface, mean):
    #Semua paramater dalam bentuk vektor
    val = 0
    temp = subtractArray(image, mean)
    for i in range(len(temp)):
        val += (eigenface[i]*temp[i])
    return val 

def calculateOmegaVector(eigenface_array, image, mean):
    M = len(eigenface_array)
    for i in range(M):
        temp = calculateOmega(eigenface_array[i])
        
        

matrix = [[1,5,9],
          [2,6,10],
          [3,7,11],
          [4,8,12]]

array = [[1],
         [2],
         [3]]

test = getEigenface(matrix, array)

print(test)

    
            
    