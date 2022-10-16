import os
import cv2
import numpy as np
from skimage.filters.rank import entropy
from skimage.morphology import disk
from sklearn.cluster import KMeans
import logging
import requests
from collections import Counter
import warnings

# ================================ FEATURES ==================================
# This class takes 3 parameters, filename, filepath and url. filename is the
# only required, but a filepath or URL needs to be given to have it work.

# Start by running .run(), this will have the program collect our features
# and can return them as a dict through .features(). you should also run .clean()
# afterwards to ensure that the image is deleted from our server.

# https://github.com/dakvaol/vis.features/blob/main/backend/features.py
# This class was inspired by David's master thesis linked above.
# Main changes: Made it a class, and added some methods for output of data,
# added methods for managing files, and changed the logic to befit a class.
# The program extracts the following features:
# - Sharpness
# - Saturation
# - Brightness
# - Entropy
# - Contrast
# - Colorfulness

# These can be accessed individually, or as a dict through self.features()


class Features:
    def __init__(self, filename, filepath=None, url=None):
        self.filename = filename
        self.filepath = filepath
        self.img_processed = None
        self.url = url

        # Misc
        self.temporary_images = 'temporary_images'
        self.__is_cleaned = False

        # Features
        self.sharpness = None
        self.saturation = None
        self.brightness = None
        self.entropy = None
        self.contrast = None
        self.colorfulness = None

    @staticmethod
    def __average(l):
        return sum(l) / len(l)

    # Makes a list of unique values from a list
    @staticmethod
    def __unique(list1):
        # Init null list
        unique_list = []

        for x in list1:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list

    def __load_image(self):
        try:
            self.img_processed = cv2.imread(self.filepath)
        except Exception as e:
            logging.error(e)
            return None

    def features(self):
        features = {
            'sharpness': self.sharpness,
            'saturation': self.saturation,
            'brightness': self.brightness,
            'entropy': self.entropy,
            'contrast': self.contrast,
            'colorfulness': self.colorfulness
        }
        if not self.__is_cleaned:
            warnings.warn('Image is not removed from server, if not intentional, please run .stop() on your object to clean the server',
                          ResourceWarning)
        return features

    # Calculates brightness by splitting HSV color space into
    # hue, saturation, and value. The value is synonymous with brightness.
    def get_brightness(self):
        image = self.img_processed.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        _, _, v = cv2.split(hsv)
        np_sum = np.sum(v, dtype=np.float32)
        num_of_pixels = v.shape[0] * v.shape[1]

        return (np_sum * 100.0) / (num_of_pixels * 255.0)

    # Calculates saturation by splitting HSV color space into
    # hue, saturation, and value. Saturation is extracted and represents
    # saturation
    def get_saturation(self):
        image = self.img_processed.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # cv2.imshow('Image', hsv)
        _, s, _ = cv2.split(hsv)
        sum = np.sum(s, dtype = np.float32)
        num_of_pixels = s.shape[0] * s.shape[1]
        return (sum * 100.0) / (num_of_pixels * 255.0)

    # Calculates entropy
    def get_entropy(self):
        image = self.img_processed.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        entropy_img = entropy(gray,disk(5))
        all_sum = np.sum(entropy_img, dtype = np.float32)
        num_of_pixels = entropy_img.shape[0] * entropy_img.shape[1]
        return all_sum / num_of_pixels

    # Calculates image sharpness by the variance of the Laplacian
    def get_sharpness(self):
        image = self.img_processed.copy()
        img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(img2gray, cv2.CV_64F).var()

    # Return contrast (RMS contrast)
    def get_contrast(self):
        image = self.img_processed.copy()
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return img_gray.std()

    def get_colorfulness(self):
        image = self.img_processed.copy()
        # split the image into its respective RGB components
        (B, G, R) = cv2.split(image.astype("float"))
        # compute rg = R - G
        rg = np.absolute(R - G)
        # compute yb = 0.5 * (R + G) - B
        yb = np.absolute(0.5 * (R + G) - B)
        # compute the mean and standard deviation of both `rg` and `yb`
        (rbMean, rbStd) = (np.mean(rg), np.std(rg))
        (ybMean, ybStd) = (np.mean(yb), np.std(yb))
        # combine the mean and standard deviations
        std_root = np.sqrt((rbStd ** 2) + (ybStd ** 2))
        mean_root = np.sqrt((rbMean ** 2) + (ybMean ** 2))
        # derive the "saturation" metric and return it
        return std_root + (0.3 * mean_root)

    def get_image_colors(self):
        pal = []
        column_names = [f'color_channel_{i}' for i in range(5*3)]
        image = self.img_processed.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image[::10, ::10]

        image = image.reshape((image.shape[0] * image.shape[1], 3))

        for tup in image:
            pal.append(tup)

        clt = KMeans(n_clusters = 5)
        clt.fit(pal)
        count = dict(Counter(clt.labels_))
        count = sorted(count.items(), key=lambda x:x[1])
        sortdict = dict(count)
        position = list(sortdict.keys())
        centers = clt.cluster_centers_ # .flatten().tolist()
        cols = centers[position].flatten().tolist()

        return dict(zip(column_names, cols))

    # Trims edges from images
    def trim(self, frame):
        # crop top
        if not np.sum(frame[0]):
            return self.trim(frame[1:])
        # crop bottom
        elif not np.sum(frame[-1]):
            return self.trim(frame[:-2])
        # crop left
        elif not np.sum(frame[:,0]):
            return self.trim(frame[:,1:])
        # crop right
        elif not np.sum(frame[:,-1]):
            return self.trim(frame[:,:-2])
        return frame

    def get_content(self):
        # Downloads the image for processing.
        img_data = requests.get(self.url).content
        self.filepath = self.temporary_images + self.filename

        with open(self.filepath, 'wb') as handler:
            handler.write(img_data)

    def get_image_features(self, scale_percent):
        if not self.img_processed:
            self.__load_image()

        scale_percent = scale_percent # percent of original size
        width = int(self.img_processed.shape[1] * scale_percent / 100)
        height = int(self.img_processed.shape[0] * scale_percent / 100)
        dim = (width, height)

        self.img_processed = cv2.resize(self.img_processed, dim, interpolation = cv2.INTER_AREA)

        self.sharpness = self.get_saturation()
        self.saturation = self.get_brightness()
        self.brightness = self.get_entropy()
        self.entropy = self.get_sharpness()
        self.contrast = self.get_contrast()
        self.colorfulness = self.get_colorfulness()

    def delete_image(self):
        os.remove(self.filepath)

    def stop(self):
        # Deletes image after processing, we have no need to store it locally.
        self.__is_cleaned = True
        self.delete_image()

    def run(self):
        # Starts class
        if self.url:
            self.get_content()
        elif self.filepath:
            self.get_image_features(100)

        else:
            print('Missing filename or URL')
            return None
