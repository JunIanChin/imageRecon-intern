import cv2
import numpy as np
import glob
import os


def masking(folder_path):
    """
    This function takes in images and then uses opencv method to do image processing to filter out noise by creating identical object 
    on a new image. This function is only used for auto3D.py.

    @param: img folder path for resized image
    """

    #assuming path folder
    img_path = folder_path + "/resized"
    masked_path = folder_path + "/masked"

    # creating a folder to store the masked images
    if not os.path.isdir(masked_path):
        os.mkdir(masked_path)

    os.chdir(img_path)

    files = glob.glob("*.jpg")

    # go through file 1 by 1
    for i in range(len(files)):
        read_im = cv2.imread("resized{}.jpg".format(i))
        edges = cv2.Canny(read_im, 20, 40)

        img_out = "masked{}.jpg".format(i)

        kernel = np.ones((5, 5), np.uint8) / 5
        opening = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # creating a frame to avoid direct contour contact with the frame of image 
        cv2.rectangle(opening, (0, 0), (599, 399), (255, 255, 255), 6)

        
        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # creating new identical dimension of image of the original image 
        mask = np.ones(read_im.shape, dtype=np.uint8)*255

        for j in range(len(contours)):
            ## filtering out contour size which we don't want , which is the noises
            if 1000 < cv2.contourArea(contours[j]) < 150000:
                #cv2.drawContours(read_im, contours, j, (0, 255, 0), 6)
                cv2.drawContours(mask, contours, j, (0,0,0), -1)

                cv2.imwrite(os.path.join(masked_path, img_out), img=mask)

    return
