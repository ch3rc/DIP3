"""
Author:     Cody Hawkins
Class:      CS5420: Digital Image Processing
Date:       Oct 11, 2020
File:       Assignment 3
"""

import getopt
import sys
import os
import cv2 as cv
import numpy as np


def help():
    print("\t\t-------HELP--------")
    print("-s, --sampling_method\t\t[1: pixel deletion/replication] [2: pixel averaging/interpolation] [default: 1]")
    print("-d, --depth\t\tNumber of levels for downsampling [default: 1]")
    print("-i, --intensity\t\tIntensity levels between 1 and 7 [default: 1]")
    print("Provide image file name you wish to test")


def filesearch(filename, search):
    # search through files and return path of image
    result = []
    for root, dirs, files in os.walk(search):
        if filename in files:
            result.append(os.path.join(root, filename))

    return result[0]


def downsample(image, sample_type, level):
    if sample_type == 1:
        # downsample by deleting every other row and column
        for _ in range(level):
            R, C = image.shape[:2]

            for i in range(0, int(R / 2)):
                image = np.delete(image, i + 1, 0)

            for i in range(0, int(C / 2)):
                image = np.delete(image, i + 1, 1)

        return image

    if sample_type == 2:
        # down sample by pixel averaging
        rows, cols = image.shape[:2]
        half_rows = rows // 2
        half_cols = cols // 2
        new_array = np.zeros((int(rows/2), int(cols/2), 3), dtype="uint8")

        for i in range(1, half_rows + 1):
            for j in range(1, half_cols + 1):
                k = i * 2
                p = j * 2
                temp = ((image[k-2, p-2] // 2) + (image[k-2,p-1] // 2))
                temp2 = ((image[k-1,p-2] // 2) + (image[k-1, p-1] // 2))
                new_array[i-1, j-1] = (temp // 2) + (temp2 // 2)

        if level > 1:
            return downsample(new_array, sample_type, level - 1)
        if level == 1:
            return new_array


def upsample(image, sample_type, level):
    if sample_type == 1:
        # upsample by inserting every other row and column
        for _ in range(level):
            R, C = image.shape[:2]

            for i in range(0, int(R * 2), 2):
                image = np.insert(image, i + 1, image[i, :], 0)

            for j in range(0, int(C * 2), 2):
                image = np.insert(image, j + 1, image[:, j], 1)
        return image

    if sample_type == 2:
        # upsample by nearest neighbor interpolation
        R, C = image.shape[:2]
        new_row = R * 2
        new_col = C * 2
        new_image = np.zeros((new_row, new_col, 3), dtype="uint8")
        for i in range(new_row):
            for j in range(new_col):
                new_image[i, j] = image[i // 2, j // 2]
        if level > 1:
            return upsample(new_image, sample_type, level - 1)
        elif level == 1:
            return new_image


def intensity_correction(image, level):
    # gamma level intensity correction
    gamma_levels = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    corrected = np.array(255 * (image / 255) ** gamma_levels[level - 1], dtype="uint8")

    return corrected


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:d:i:", ["help", "sampling_method", "depth", "intensity"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    sampling_method = 1
    depth = 1
    intensity = 1
    img_name = None

    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit(1)
        elif o in ("-s", "--sampling_method"):
            sampling_method = int(a)
            if sampling_method < 1:
                sampling_method = 1
            elif sampling_method > 2:
                sampling_method = 2
        elif o in ("-d", "--depth"):
            depth = int(a)
            if depth < 1:
                depth = 1
            elif depth > 7:
                depth = 7
        elif o in ("-i", "--intensity"):
            intensity = int(a)
            if intensity < 1:
                intensity = 1
            elif intensity > 7:
                intensity = 7
        else:
            assert False, "Unhandled Option!"

    if len(args) > 0:
        img_name = args[0]
        search = "C:\\Users\\codyh\\PycharmProjects\\DIP2\\test"
        name = filesearch(img_name, search)

    if os.path.exists(name):
        try:
            img = cv.imread(name)
            small = downsample(img, sampling_method, depth)
            large = upsample(small, sampling_method, depth)
            small = intensity_correction(small, intensity)
            large = intensity_correction(large, intensity)
            print("small: ", small.shape)
            print("large: ", large.shape)
            cv.imshow("small image", small)
            cv.imshow("large image", large)
            cv.waitKey(0)
        except cv.error as err:
            print(err)
            sys.exit(1)


if __name__=="__main__":
    main()