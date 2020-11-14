"""
This module contains simple helper methods.
"""
import time
import numpy as np
import cv2


def show(image, title='image', delay=0):
    """
    Show image on the screen.
    """
    title += ', ' + str(np.shape(image))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(delay)

def dump(image, name='image'):
    """
    Save image to the PNG file.
    """
    timestamp = int(round(time.time() * 1000))
    file_path = './dump/' + name + '_' + str(timestamp) + '.png'
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(file_path, image)
