import cv2 
import glob 
import os 


def resize(img_list):
    """
    This function takes in image folder path and resize each image to a standard dimension.
    """
    img_path = os.getcwd().replace(os.sep,'/')
    output_path = img_path + '/resized'

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    for i in range(len(img_list)):
        resized = 'resized{}.jpg'.format(i)
        tmp = cv2.imread(img_list[i])
        gray = cv2.cvtColor(tmp , cv2.COLOR_BGR2GRAY)
        converted = cv2.resize(gray,(600,400))
        cv2.imwrite(os.path.join(output_path,resized),img = converted)
        i +=1

    return