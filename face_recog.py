import image_handler as ih
import euclidean_distance as ed
import numpy as np

def RunFaceRecognition(dataset_path, test_path):
    datasetImageArr, datasetImageName = ih.collect_image(256, dataset_path)
    print("Dataset collected")
    print("Image size: ", len(datasetImageArr))
    
    image_mean = np.array(ed.arrayMeanInt(datasetImageArr))
    image_diff = np.array([[]])
    image_diff = np.append(image_diff, [ed.subtractArray(datasetImageArr[0], image_mean)], axis = 1)
    for i in range(1, len(datasetImageArr)):
        image_diff = np.append(image_diff, [ed.subtractArray(datasetImageArr[i], image_mean)], axis = 0)
    image_diff_transpose = np.transpose(image_diff)
    covariance = np.matmul(image_diff, image_diff_transpose)
    
RunFaceRecognition("./dataset/pins_Elizabeth Lail", "./dataset/pins_Elizabeth Lail/Elizabeth Lail1.jpg")