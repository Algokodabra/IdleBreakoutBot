"""
This module contains class FramesProvider allowing to acquire frames by using take_frame() method.
These frames can be either images, which have been read from the disk, or the screen snapshots.
"""
import os
import enum
import numpy as np
import cv2
import pyautogui as gui


class FrameSources(enum.Enum):
    """
    Enum of possible frame sources.
    """
    FILE = 0
    SCREEN = 1

class FramesProvider:
    """
    This class allows to grab frames from different sources.
    """
    def __init__(self, frame_source=FrameSources.SCREEN, images_dir_path=None):
        self.frame_source = frame_source
        self.frames = []
        self.current_frame_index = 0
        if self.frame_source == FrameSources.FILE:
            if not isinstance(images_dir_path, str):
                raise Exception('`images_dir_path` should be a string path to the directory with images')
            file_names_list = os.listdir(images_dir_path)
            if len(file_names_list) == 0:
                raise Exception('`images_dir_path` does not have any files')
            for file_name in file_names_list:
                image_file_path = os.path.join(images_dir_path, file_name)
                image = cv2.cvtColor(cv2.imread(image_file_path), cv2.COLOR_BGR2RGB)
                self.frames.append(image)

    def take_frame(self):
        """
        Get single frame. Source of the frame depends on the current value of the self.frame_source.

        Returns:
            NumPy array: Frame.
        """

        if self.frame_source == FrameSources.FILE:
            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0
            frame = self.frames[self.current_frame_index]
            self.current_frame_index += 1
        else:
            frame = np.array(gui.screenshot())
        return frame
