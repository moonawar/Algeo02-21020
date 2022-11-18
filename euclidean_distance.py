import numpy as np
from matplotlib import pyplot as plt

def euclidean_distance(v1,v2):
    #I.S. len(v1) = len(v2), v1 v2 array linear
    # Mengembalikan euclidean_distance dari v1 v2 (float)
    result = 0
    for i in range(len(v1)):
        result += (v1[i]-v2[i])**2
    result /= (result)**0.5
    return result



def sum2Array(array1, array2):
    #Syarat
    #len(array1)==len(array2)
    array3 = []
    for i in range(len(array1)):
        array3.append(array1[i]+array2[i])
    return array3



#use np.mean(0) instead
def arrayMeanInt(array_of_image):
    print("Getting Mean image")
    #I.S. Array yang berisi vektor gambar
    #Rata - Rata yang dihasilkan di floor
    array_of_imageO = []
    k = len(array_of_image)
    for i in range(len(array_of_image[0])):
        print("Baris " + str(i))
        sum = 0
        count = 0
        for j in range(k):
            sum+= array_of_image[j][i]
        array_of_imageO.append(sum//k)
    return array_of_imageO
             
"""
Method 1: problem ineff
array_of_imageO = array_of_image[0]
count = 1
for i in range(1,len(array_of_image)):
    array_of_imageO = sum2Array(array_of_imageO, array_of_image[i])
    count +=1
for i in rang e(len(array_of_imageO)):
    array_of_imageO[i]//=count
return array_of_imageO
"""






def subtractArray(array1, array2):
    array = []
    for i in range(len(array1)):
        array.append(array1[i]-array2[i])
    return array

def findMinDistance(dataset_omega, test_omega):
    # Mengembalikan index yang euclidean distancenya paling kecil dengan val
    min = euclidean_distance(test_omega, dataset_omega[0])
    index = 0
    for i in range(len(dataset_omega)):
        temp = euclidean_distance(dataset_omega[i], test_omega)
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
    eigenFaces = np.matmul(np.transpose(array_of_images), np.transpose(eigenVector))
    eigenFaces = np.transpose(eigenFaces)
    return eigenFaces





def get_column(array_of_images, index):
    vectors = []
    for i in range(array_of_images.shape[0]):
        vectors.append(array_of_images[i][0])
    return vectors

def calculateOmega(image, eigenface, mean):
    #Semua paramater dalam bentuk vektor
    print(image.shape)
    temp = np.subtract(image, mean)
    val = np.dot(temp,eigenface)
    return val 

def calculateOmegaVector(eigenface_array, image, mean):
    array = []
    for i in range(len(eigenface_array)):
        temp = calculateOmega(image, eigenface_array[i], mean)
        array.append(temp)
    return array
        
def displayIMG(vector):
    arr = vector
    arr = np.reshape(arr, (256,256))
    plt.imshow(arr, cmap="gray")
    plt.show()
    
    
    

matrix = [[1,5,9],
          [2,6,10],
          [3,7,11],
          [4,8,12]]

array = [[1],
         [2],
         [3]]

#test = getEigenface(matrix, array)




array1 = [1,2,3]
array2 = [4,5,6]
print(sum2Array(array1, array2))

print(np.mean(matrix, axis=1))
    
            
    