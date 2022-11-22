from euclidean_distance import findMinDistance
from face_recog import GetDatasetOmega, GetTestImageOmega
from image_handler import collect_image, transformMtoA
import numpy as np
import cv2 as cv

# Main Process
def test():
    #Get img
    img_array, img_name = collect_image( 256,"../test/dataset")

    ori_img = img_array
    mean = img_array.mean(axis=0)

    #subtract all img_array
    for i in range(len(img_array)):
        img_array[i] = np.subtract(img_array[i], mean)
        
    #Find eigen of  AT A
    transposed = np.transpose(img_array)
    Cov = np.matmul(img_array, transposed)
    w,v = np.linalg.eig(Cov)
    eigen_vector = []
    for i in range(93):
        eigen_vector.append(np.reshape(v[:,i], (93)))


    #Get eigen face
    face = np.transpose(np.dot(np.transpose(img_array), np.transpose(eigen_vector)))
    print(face.shape)

    #Get omega matrix
    omega = []
    for i in range(len(ori_img)):
        temp = GetDatasetOmega(face, ori_img[i], mean)
        omega.append(temp)
    print(omega)
    #get test image
    test_img = cv.imread("../test/test images/Tom Holland6_4843.jpg", 0)
    test_img = cv.resize(test_img, (256,256))
    test_img = transformMtoA(test_img)

    test_omega = GetTestImageOmega(face, test_img, mean)

    x = findMinDistance(omega, test_omega)
    return x

main_process()
print("Done")
