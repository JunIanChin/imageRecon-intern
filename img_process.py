import cv2
import numpy as np
import glob
import os


def img_process(folder_path):
    """
    This function is linked to gui.py , it gets the user selection folder and masked the images . the functionality is same with masking.py
    """
    ori_path = os.getcwd().replace(os.sep,'/')
    masked_path = ori_path + "/masked"

    if not os.path.isdir(masked_path):
        os.mkdir(masked_path)

    os.chdir(folder_path)

    files = glob.glob("*.jpg")

    for i in range(len(files)):
        read_im = cv2.imread("resized{}.jpg".format(i))
        edges = cv2.Canny(read_im, 20, 40)

        img_out = "masked{}.jpg".format(i)

        kernel = np.ones((5, 5), np.uint8) / 5
        opening = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        cv2.rectangle(opening, (0, 0), (599, 399), (255, 255, 255), 6)

       
        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        mask = np.ones(read_im.shape, dtype=np.uint8)*255

        for j in range(len(contours)):
            if 1000 < cv2.contourArea(contours[j]) < 150000:
                #cv2.drawContours(read_im, contours, j, (0, 255, 0), 6)
                cv2.drawContours(mask, contours, j, (0,0,0), -1)

                cv2.imwrite(os.path.join(masked_path, img_out), img=mask)

    return
