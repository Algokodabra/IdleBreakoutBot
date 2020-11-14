"""
This script allows to automate basic gameplay of the Idle Breakout game.
https://armorgames.com/idle-breakout-game/18584
"""
import time
import numpy as np
import cv2
import pyautogui as gui
from utils import show, dump
from frames_provider import FramesProvider, FrameSources


def detect_bricks(
    image, black_threshold, brick_min_area, brick_circularity_range, show_images, dump_images
):
    """
    Compute coordinates of brick centers.
    """

    # Convert the image to grayscale.
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Make the image binary by thresholding it with the black_threshold value.
    _, image_binary = cv2.threshold(image_gray, black_threshold, 255, cv2.THRESH_BINARY_INV)

    # Find all closed contours on the binary image.
    contours, _ = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Filter contours by area and circularity to leave only brick contours.
    brick_contours = []
    brick_contours_indices = []  # For debug only.
    contour_index = -1  # For debug only.
    for contour in contours:
        contour_index += 1
        area = cv2.contourArea(contour)
        if area < brick_min_area:
            continue
        perimeter = cv2.arcLength(contour, closed=True)
        circularity = 4.0 * np.pi * area / (perimeter ** 2.0)
        if brick_circularity_range[0] < circularity < brick_circularity_range[1]:
            brick_contours.append(contour)
            brick_contours_indices.append(contour_index)

    # For each brick contour get the center of its bounding box.
    bricks = []
    for contour in brick_contours:
        box_x, box_y, box_width, box_height = cv2.boundingRect(contour)
        bricks.append((box_x + box_width // 2, box_y + box_height // 2))

    if show_images or dump_images:
        #contours_colors = [[255, 255, 0]] * len(contours)
        contours_colors = 255 * np.random.rand(len(contours), 3)
        image_contours = cv2.merge((image_gray,) * 3)
        for i in range(len(contours)):
            image_contours = cv2.drawContours(image_contours, contours, i, contours_colors[i], -1)
        image_brick_contours = cv2.merge((image_gray,) * 3)
        for i in brick_contours_indices:
            image_brick_contours = cv2.drawContours(image_brick_contours, contours, i, contours_colors[i], -1)
        image_bricks = cv2.merge((image_gray,) * 3)
        for brick in bricks:
            image_bricks = cv2.drawMarker(image_bricks, brick, (255, 255, 0), cv2.MARKER_CROSS, thickness=2)

        if show_images:
            show(image, '1. image', 1)
            show(image_gray, '2. image_gray', 1)
            show(image_binary, '3. image_binary', 1)
            show(image_contours, '4. image_contours', 1)
            show(image_brick_contours, '5. image_brick_contours', 1)
            show(image_bricks, '6. image_bricks', 0)

        if dump_images:
            dump(image, '1_image')
            dump(image_gray, '2_image_gray')
            dump(image_binary, '3_image_binary')
            dump(image_contours, '4_image_contours')
            dump(image_brick_contours, '5_image_brick_contours')
            dump(image_bricks, '6_image_bricks')

    return bricks

def get_list_of_ready_buttons(
    image, first_ball_button_position, ball_buttons_x_step, ball_buttons_number, ball_button_ready_color
):
    """
    Get list of coordinates of active buttons.
    """

    ready_buttons = []
    for i in range(ball_buttons_number):
        button_position = first_ball_button_position + i * np.array([ball_buttons_x_step, 0])
        button_color = image[button_position[1], button_position[0], :]
        if np.all(button_color == ball_button_ready_color):
            ready_buttons.append(button_position)

    return ready_buttons

if __name__ == '__main__':
    # Define constants.
    FRAMES_LIMIT = 1
    FIRST_BUTTON_POSITION = np.array([255, 130])
    BUTTONS_X_STEP = 71
    BUTTONS_NUMBER = 6
    BUTTON_READY_COLOR = np.array([85, 212, 0])
    BLACK_THRESHOLD = 25
    BRICK_MIN_AREA = 100
    BRICK_CIRCULARITY_RANGE = (0.71, 0.75)
    SHOW_IMAGES = True
    DUMP_IMAGES = False
    ONLY_DETECT_BRICKS = True

    # Initialize frame provider.
    frames_provider = FramesProvider(FrameSources.FILE, './frames/level1')

    # Start the main loop.
    time.sleep(3.0)
    for frame_index in range(FRAMES_LIMIT):
        print('frame ', frame_index)
        frame = frames_provider.take_frame()

        if not ONLY_DETECT_BRICKS:
            ready_buttons_list = get_list_of_ready_buttons(
                frame, FIRST_BUTTON_POSITION, BUTTONS_X_STEP, BUTTONS_NUMBER, BUTTON_READY_COLOR
            )
            if len(ready_buttons_list) > 0:
                gui.moveTo(ready_buttons_list[0][0], ready_buttons_list[0][1], duration=2.0)
                gui.mouseDown()
                gui.mouseUp()

        detected_bricks = detect_bricks(
            frame, BLACK_THRESHOLD, BRICK_MIN_AREA, BRICK_CIRCULARITY_RANGE, SHOW_IMAGES, DUMP_IMAGES
        )

        if not ONLY_DETECT_BRICKS:
            if len(detected_bricks) == 0:
                break
            gui.moveTo(detected_bricks[0][0], detected_bricks[0][1], duration=0.2)
            gui.mouseDown()
            gui.mouseUp()
