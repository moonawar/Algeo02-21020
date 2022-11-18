from euclidean_distance import getEigenface, displayIMG, arrayMeanInt, subtractArray

from image_resize import collect_image
import numpy as np

img_array, img_name = collect_image( 256,"./dataset")




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


Cov = np.matmul(np.matrix(img_array), np.matrix(transposed))


print(Cov.shape)

w,v = np.linalg.eig(Cov)

#print(w)
vector = np.transpose(v[0])


face = getEigenface(vector,img_array)


print("Done")
