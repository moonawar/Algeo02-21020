import image_handler as ih
import euclidean_distance as ed
import numpy as np
import eigen as e

def RunFaceRecognition(dataset_path, test_path):
    datasetImageArr, datasetImageName = ih.collect_image(256, dataset_path)
    print("Dataset collected")
    print("Image size: ", len(datasetImageArr))
    
    image_mean = np.array(ed.arrayMeanInt(datasetImageArr))
    image_diff_transpose = np.array([[]])
    image_diff_transpose = np.append(image_diff_transpose, [ed.subtractArray(datasetImageArr[0], image_mean)], axis = 1)
    for i in range(1, len(datasetImageArr)):
        image_diff_transpose = np.append(image_diff_transpose, [ed.subtractArray(datasetImageArr[i], image_mean)], axis = 0)

    image_diff = np.transpose(image_diff_transpose)
    covariance_op = np.matmul(image_diff_transpose, image_diff)
    eigen_values, eigen_vectors_op = e.get_eigen(covariance_op)
    eigen_vectors = np.matmul(image_diff, eigen_vectors_op)
    print(f"Eigen vectors calculated : {eigen_vectors.shape}")
    print(eigen_vectors)
    
    
RunFaceRecognition("./dataset/pins_Elizabeth Lail", "./dataset/pins_Elizabeth Lail/Elizabeth Lail1.jpg")