import numpy as np
import euclidean_distance as ed
from math import sqrt

def QR_decomposition(mat):
    # I.S. matriks mat adalah matriks persegi
    # F.S. mengembalikan matriks Q dan R yang merupakan hasil QR decomposition
    #      dari matriks mat

    Q = np.zeros((mat.shape[0], mat.shape[1]))
    R = np.zeros((mat.shape[0], mat.shape[1]))
    
    for i in range(mat.shape[0]):
        # Ambil kolom i dari matriks mat
        Q[:, i] = mat[:, i]
        for j in range(i):
            # Hitung dot product antara kolom i dan kolom j
            R[j, i] = np.dot(Q[:, j], mat[:, i])
            # Kurangi kolom i dengan dot product kali kolom j
            Q[:, i] = Q[:, i] - R[j, i] * Q[:, j]
        # Hitung norm dari kolom i
        R[i, i] = vector_length(Q[:, i])
        # Normalisasi kolom i
        Q[:, i] = Q[:, i] / R[i, i]

    return Q, R

def isUpperTriangular(mat):
    # I.S. matriks mat adalah matriks persegi
    # F.S. mengembalikan True jika matriks mat adalah matriks segitiga atas
    #      dan False jika sebaliknya. Digunakan tresshold 0.0005 untuk menentukan
    #      apakah suatu elemen matriks mat adalah 0 atau tidak
    
    for i in range(1, mat.shape[0]):
        for j in range(i):
            if abs(mat[i, j]) > 0.0005:
                return False
    return True

def get_eigen_values(mat):
    # I.S. matriks mat adalah matriks persegi
    # F.S. mengembalikan nilai eigen dari matriks mat
    
    # Metode yang dimanfaatkan adalah metode QR decomposition
    # Referensi : https://www.youtube.com/watch?v=tYqOrvUOMFc

    mat = np.array(mat)
    eigen_values = []
    matQ, matR = QR_decomposition(mat)
    iterationMat = np.matmul(matR, matQ)

    max_iteration = 4 * mat.shape[0]
    iteration = 0

    # Iterasi sampai matriks iterationMat adalah matriks segitiga atas atau 
    # mencapai maksimum iterasi
    while not isUpperTriangular(iterationMat) and iteration < max_iteration:
        matQ, matR = QR_decomposition(iterationMat)
        iterationMat = np.matmul(matR, matQ)
        iteration += 1

    # Ambil diagonal dari matriks iterationMat sebagai nilai eigen
    for i in range(iterationMat.shape[0]):
        eigen_values.append(iterationMat[i, i])

    return np.array(eigen_values)

def get_eigen_vectors(mat, eigen_values):
    # I.S. matriks mat adalah matriks persegi dan eigen_values adalah array
    #      yang berisi nilai eigen dari matriks mat

    # F.S. mengembalikan array yang berisi vektor eigen dari matriks mat

    # Metode yang digunakan adalah metode inverse power iteration
    # Referensi : https://www.youtube.com/watch?v=tYqOrvUOMFc
    max_iteration = 4 * mat.shape[0]
    eigen_vectors = np.array([[]])
    
    RANDOM_VECTOR = np.random.rand(mat.shape[0])
    IDENTITY_MATRIX = np.identity(mat.shape[0])

    i = 0
    # Cari vektor eigen untuk setiap nilai eigen yang ada
    for eigen_value in eigen_values:
        # Gunakan inverse power iteration hingga vektor eigen konvergen ke nilai yang benar
        iterationMat = np.subtract(mat, np.multiply(eigen_value, IDENTITY_MATRIX))
        if (np.linalg.det(iterationMat) == 0):
            iterationMat = np.subtract(mat, np.multiply(eigen_value + 0.0001, IDENTITY_MATRIX))
        
        iterationMat = np.linalg.inv(iterationMat)
        eigen_vector = np.matmul(iterationMat, RANDOM_VECTOR)
        eigen_vector = eigen_vector / vector_length(eigen_vector)
        iteration = 0

        # Treshold untuk menentukan apakah vektor eigen sudah konvergen atau belum
        deltaTreshold = 0.0005
        delta = 1
        
        # Proses Iterasi
        # Iterasi sampai mendapatkan vektor eigen yang konvergen atau mencapai maksimum iterasi
        while iteration < max_iteration and delta > deltaTreshold:
            prevEigenVector = eigen_vector
            eigen_vector = np.matmul(iterationMat, eigen_vector)
            eigen_vector = eigen_vector / vector_length(eigen_vector)
            delta = vector_length(np.subtract(eigen_vector, prevEigenVector))
            iteration += 1
        
        # Tambahkan vektor eigen ke array eigen_vectors
        if i == 0:
            if eigen_vector[0] < 0:
                eigen_vector = -1 * eigen_vector 
            eigen_vectors = np.append(eigen_vectors, [eigen_vector], axis = 1)
        else:
            if eigen_vector[0] < 0:
                eigen_vector = -1 * eigen_vector 
            eigen_vectors = np.append(eigen_vectors, [eigen_vector], axis = 0)
        i += 1

    return eigen_vectors

def get_eigen(mat):
    # I.S. matriks mat adalah matriks persegi
    # F.S. mengembalikan nilai eigen dan vektor eigen dari matriks mat
    eigen_values = get_eigen_values(mat)
    eigen_vectors = get_eigen_vectors(mat, eigen_values)
    return eigen_values, eigen_vectors

def get_weights(eigen_faces, image_diff):
    # I.S. eigenv_array adalah array yang berisi eigen faces dari matriks
    #      covariance dari gambar yang diambil dan image_diff adalah array
    #      yang berisi perbedaan antara gambar yang diambil dengan gambar
    #      rata-rata
    # F.S. mengembalikan array yang berisi bobot/weight dari gambar yang diambil
    #      terhadap setiap eigen faces

    # Proses untuk input gambar berupa array 2 dimensi (dataset)
    if len(image_diff.shape) != 1:
        weights = [[] for i in range(image_diff.shape[1])]
        for image in range(image_diff.shape[1]):
            for eigen_vector in range(eigen_faces.shape[0]):
                weights[image].append(np.dot(eigen_faces[eigen_vector], image_diff[:, image]))
    # Proses untuk input gambar berupa array 1 dimensi (test_image)
    else:
        weights = []
        for eigen_vector in range(eigen_faces.shape[0]):
            weights.append(np.dot(eigen_faces[eigen_vector], image_diff))
    return np.array(weights)

def vector_length(v):
    # I.S. v adalah sebuah vektor
    # F.S. mengembalikan panjang dari vektor v
    sum = 0
    for i in range(len(v)):
        sum += v[i] ** 2
    return sqrt(sum)