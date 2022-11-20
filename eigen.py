import numpy as np
import euclidean_distance as ed

def QR_decomposition(mat):
    Q = np.zeros((mat.shape[0], mat.shape[1]))
    R = np.zeros((mat.shape[0], mat.shape[1]))
    
    for i in range(mat.shape[0]):
        Q[:, i] = mat[:, i]
        for j in range(i):
            R[j, i] = np.dot(Q[:, j], mat[:, i])
            Q[:, i] = Q[:, i] - R[j, i] * Q[:, j]
        R[i, i] = np.linalg.norm(Q[:, i])
        Q[:, i] = Q[:, i] / R[i, i]

    return Q, R

def isUpperTriangular(mat):
    for i in range(1, mat.shape[0]):
        for j in range(i):
            if abs(mat[i, j]) > 0.0005:
                return False
    return True

def get_eigen_values(mat):
    mat = np.array(mat)
    eigen_values = []
    matQ, matR = QR_decomposition(mat)
    iterationMat = np.matmul(matR, matQ)

    max_iteration = 4 * mat.shape[0]
    iteration = 0

    while not isUpperTriangular(iterationMat) and iteration < max_iteration:
        matQ, matR = QR_decomposition(iterationMat)
        iterationMat = np.matmul(matR, matQ)
        iteration += 1

    for i in range(iterationMat.shape[0]):
        eigen_values.append(iterationMat[i, i])

    return eigen_values

def get_eigen_vectors(mat, eigen_values):

    max_iteration = 4 * mat.shape[0]
    eigen_vectors = np.array([[]])
    
    RANDOM_VECTOR = np.random.rand(mat.shape[0])
    IDENTITY_MATRIX = np.identity(mat.shape[0])

    i = 0
    for eigen_value in eigen_values:
        iterationMat = np.subtract(mat, np.multiply(eigen_value, IDENTITY_MATRIX))
        iterationMat = np.linalg.inv(iterationMat)

        eigen_vector = np.matmul(iterationMat, RANDOM_VECTOR)
        eigen_vector = eigen_vector / np.linalg.norm(eigen_vector)
        iteration = 0

        deltaTreshold = 0.0005
        delta = 1
        while iteration < max_iteration and delta > deltaTreshold:
            prevEigenVector = eigen_vector
            eigen_vector = np.matmul(iterationMat, eigen_vector)
            eigen_vector = eigen_vector / np.linalg.norm(eigen_vector)
            delta = np.linalg.norm(np.subtract(eigen_vector, prevEigenVector))
            iteration += 1
        
        if i == 0:
            eigen_vectors = np.append(eigen_vectors, [eigen_vector], axis = 1)
        else:
            eigen_vectors = np.append(eigen_vectors, [eigen_vector], axis = 0)
        i += 1

    return eigen_vectors

def get_eigen(mat):
    eigen_values = get_eigen_values(mat)
    eigen_vectors = get_eigen_vectors(mat, eigen_values)
    return eigen_values, eigen_vectors