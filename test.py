from euclidean_distance import getEigenface, displayIMG, arrayMeanInt, subtractArray, calculateOmegaVector, findMinDistance

from image_resize import collect_image, transformMtoA
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img_array, img_name = collect_image( 256,"./dataset")

ori_img = img_array


mean = img_array.mean(axis=0)

test = np.subtract(img_array[0],mean)# ngggak banyak berubah
#


#subtract all img_array
for i in range(len(img_array)):
    print(f"Process image {i}")
    img_array[i] = np.subtract(img_array[i], mean)

    
    
    
#Find eigen of  AT A
transposed = np.transpose(img_array)
print(img_array)
print(transposed)


Cov = np.matmul(img_array, transposed)


print(Cov.shape)
print(Cov[0])
w,v = np.linalg.eig(Cov)

#print(w)
#vector = np.transpose(v[0])
print(v.shape)
#img_array = np.transpose(img_array)

#eigen vector size of 1xM
eigen_vector = []
for i in range(93):
    eigen_vector.append(np.reshape(v[:,i], (93)))

face = np.transpose(np.dot(np.transpose(img_array), np.transpose(eigen_vector)))
print(face[0])
#for i in range(len(face)):
#    print(face[i])
print(face)
print(face.shape)
#Get omega matrix
omega = []
print(ori_img)
for i in range(len(ori_img)):
    print(i)
    temp = calculateOmegaVector(face, ori_img[i], mean)
    omega.append(temp)

#get test image
test_img = cv.imread("./test/test.jpg", 0)
test_img = cv.resize(test_img, (256,256))
test_img = transformMtoA(test_img)
test_omega = calculateOmegaVector(face, test_img, mean)

x = findMinDistance(omega, test_omega)

result = cv.imread(img_name[x])

print(result)
cv.imshow(result)

plt.imshow(result)
plt.show()


print("Done")
