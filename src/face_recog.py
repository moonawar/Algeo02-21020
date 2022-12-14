import image_handler as ih
import euclidean_distance as ed
import image_handler as ih
import numpy as np
import eigen as e

INPUT_SIZE = 512

def ExtractDataset(dataset):
    # I.S. dataset adalah array of images yang berukuran N^2 x M, dimana N adalah ukuran gambar dan M adalah jumlah gambar
    # F.S. akan direturn 3 komponen hasil ekstraksi dataset, yaitu eigen_faces, image_mean, dan image_diff
    #   -- eigen_faces adalah array of eigenfaces yang berukuran N^2 x M, dimana N adalah ukuran gambar dan M adalah jumlah eigenfaces
    #   -- image_mean adalah array of mean image yang berukuran N^2 x 1, dimana N adalah ukuran gambar
    #   -- image_diff adalah array of image difference yang berukuran N^2 x M, dimana N adalah ukuran gambar dan M adalah jumlah gambar

    # Cari image mean -------------------------------------------------
    image_mean = np.array(ed.arrayMeanInt(dataset))
    # -----------------------------------------------------------------

    
    # Cari image difference -------------------------------------------
    image_diff_transpose = np.array([[]])
    image_diff_transpose = np.append(image_diff_transpose, [ed.subtractArray(dataset[0], image_mean)], axis = 1)
    for i in range(1, len(dataset)):
        image_diff_transpose = np.append(image_diff_transpose, [ed.subtractArray(dataset[i], image_mean)], axis = 0)

    image_diff = np.transpose(image_diff_transpose)
    # -----------------------------------------------------------------

    # Cari eigenfaces -------------------------------------------------
    # Eigenfaces adalah eigen vector dari covariance matrix
    # " Covariance matrix adalah hasil perkalian antara image difference dengan transpose image difference, namun untuk efisiensi
    # digunakan perkalian transpose image difference dengan image difference. Keduanya memiliki eigen value yang sama dan eigen vectornya
    # dapat didapatkan melalui perkalian matrix image difference dengan vektor eigen dari covariance yang optimized (lebih jelasnya ada di laporan) ".
    
    # Find optimized covariance matrix
    covariance_op = np.matmul(image_diff_transpose, image_diff)
    eigen_values, eigen_vectors_op = e.get_eigen(covariance_op)

    # Get the actual eigen vector of the covariance matrix
    eigen_faces = np.matmul(image_diff, eigen_vectors_op)
    # Normalized to get the eigen faces
    for i in range(eigen_faces.shape[1]):
        eigen_faces[:, i] = eigen_faces[:, i] / e.vector_length(eigen_faces[:, i])
    eigen_faces = np.transpose(eigen_faces)
    # -----------------------------------------------------------------

    return eigen_faces, image_mean, image_diff

def GetDatasetOmega(eigen_faces, image_diff):
    # I.S. eigen_faces adalah array of eigenfaces yang berukuran N^2 x M, dimana N adalah ukuran gambar dan M adalah jumlah eigenfaces
    #      image_diff adalah array of image difference yang berukuran N^2 x M, dimana N adalah ukuran gambar dan M adalah jumlah gambar
    # F.S. akan direturn array of omega yang berukuran M x M, dimana M adalah jumlah eigenfaces
    weights = e.get_weights(eigen_faces, image_diff)
    return weights

def GetTestImageOmega(eigen_faces, test_image, image_mean):
    # I.S. eigen_faces adalah array of eigenfaces yang berukuran N^2 x M, dimana N adalah ukuran gambar dan M adalah jumlah eigenfaces
    #      test_image adalah array of test image yang berukuran N^2 x 1, dimana N adalah ukuran gambar
    #      image_mean adalah array of mean image yang berukuran N^2 x 1, dimana N adalah ukuran gambar
    # F.S. akan direturn array of omega yang berukuran M x 1, dimana M adalah jumlah eigenfaces
    image_diff = np.subtract(test_image, image_mean)
    return e.get_weights(eigen_faces, image_diff)

def ReconstructImage(eigen_faces, dataset_mean, test_image_weights):
    image = 2 * dataset_mean / 2  # This simple trick is to make a copy of the array without contaminating the original array
    for i in range(len(test_image_weights)):
        image = image + ( eigen_faces[i] * test_image_weights[i] )

    image = ih.transformAtoM(image, INPUT_SIZE)
    return image

def FaceRecognition(dataset_path, test_path):
    # I.S. dataset_path adalah path dari dataset yang berisi gambar-gambar wajah
    #      test_path adalah path dari gambar wajah yang akan diidentifikasi
    # F.S. akan direturn path wajah yang terdeteksi dari gambar test_path
    import app

    app.updateSummary("Loading dataset...")
    # Load dataset ----------------------------------------------------
    datasetImageArr, datasetImageName = ih.collect_image(INPUT_SIZE, dataset_path)
    testImage = ih.get_image(INPUT_SIZE, test_path)
    # -----------------------------------------------------------------

    app.updateSummary("Extracting dataset...")
    # Ekstraksi dataset -----------------------------------------------
    eigen_faces, image_mean, image_diff = ExtractDataset(datasetImageArr)
    app.eigen_faces = eigen_faces
    app.dataset_mean = image_mean
    # -----------------------------------------------------------------

    # Cari omega dari dataset dan image test --------------------------
    app.updateSummary("Get dataset weights...")
    datasetWeights = GetDatasetOmega(eigen_faces, image_diff)

    app.updateSummary("Get test image weights...")
    testImageWeights = GetTestImageOmega(eigen_faces, testImage, image_mean)
    app.test_image_weights = testImageWeights
    # -----------------------------------------------------------------

    # Cari jarak euclidean dari image test ke setiap image dataset ----
    # Ambil index dari image dataset dengan jarak euclidean terkecil
    app.updateSummary("Looking for the closest Images...")
    image_index = ed.findMinDistance(datasetWeights, testImageWeights)
    app.image_index = image_index
    # -----------------------------------------------------------------

    # Return path dari image dataset yang terdeteksi sebagai wajah yang sama/dekat dengan image test
    # Jika tidak ada yang mirip, return -1
    if image_index == -1:
        return -1
    else:
        closest_image = ""
        for c in datasetImageName[image_index]:
            if c == "/" or c == "\\":
                closest_image = ""
            else:
                closest_image += c
        app.updateSummary("The closest image from the dataset is: " + closest_image)
        return datasetImageName[image_index]