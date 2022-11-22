import numpy as np
from matplotlib import pyplot as plt
import eigen as e

def euclidean_distance(v1, v2):
    # I.S. len(v1) = len(v2), v1 dan v2 adalah array linear
    # Mengembalikan euclidean_distance dari v1 dan v2 --> (float)
    result = 0
    for i in range(len(v1)):
        result += (v1[i] - v2[i]) ** 2
    
    if result == 0:
        return 0
    else:
        result /= (result) ** 0.5
        return result

def arrayMeanInt(array_of_image):
    # I.S. Array yang berisi vektor gambar
    # Rata - Rata yang dihasilkan di floor
    array_of_imageO = []
    k = len(array_of_image)
    for i in range(len(array_of_image[0])):
        sum = 0
        count = 0
        for j in range(k):
            sum+= array_of_image[j][i]
        array_of_imageO.append(sum / k)
    return array_of_imageO

def subtractArray(array1, array2):
    array = []
    for i in range(len(array1)):
        array.append(array1[i]-array2[i])
    return array

def findDatasetOmegaRange(omega_dataset):
    # Mengembalikan nilai range dari dataset omega
    # I.S. omega_dataset adalah array yang berisi vektor omega
    # F.S. Mengembalikan nilai range dari dataset omega
    omegaRange = euclidean_distance(omega_dataset[0], omega_dataset[1])
    
    for i in range(len(omega_dataset)):
        for j in range(len(omega_dataset)):
            temp = euclidean_distance(omega_dataset[i], omega_dataset[j])
            if omegaRange < temp:
                omegaRange = temp
            else:
                continue
    return omegaRange
    
def findMinDistance(dataset_omega, test_omega):
    # Mengembalikan index yang euclidean distancenya paling kecil dengan value
    min = euclidean_distance(test_omega, dataset_omega[0])
    index = 0
    for i in range(len(dataset_omega)):
        temp = euclidean_distance(dataset_omega[i], test_omega)
        if min > temp:
            min = temp
            index = i
        else:
            continue
    
    TOLERANCE_LEVEL = findDatasetOmegaRange(dataset_omega) // 2 
    if min > TOLERANCE_LEVEL:
        return -1
    return index

def getEigenface(array_of_images, eigenVector):
    # yang dipake crossproduct of normalized array of images and eigenVector
    
    eigenFaces = np.matmul(np.transpose(array_of_images), np.transpose(eigenVector))
    eigenFaces = np.transpose(eigenFaces)
    return eigenFaces

def get_column(array_of_images, index):
    vectors = []
    for i in range(array_of_images.shape[0]):
        vectors.append(array_of_images[i][0])
    return vectors
        
def displayIMG(vector):
    arr = vector
    arr = np.reshape(arr, (256,256))
    plt.imshow(arr, cmap="gray")
    plt.show()