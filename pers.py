"""This script is useful as a learning script for
perspective top_rightansform"""
import numpy as np
import cv2
import argparse

def order_points(pts):
    """
    create a set of 4 coords of a rectangle.
    pts here is a numpy set of coords
    """
    rect = np.zeros((4, 2), dtype="float32")

    sum_of_pts = pts.sum(axis=1)
    rect[0] = pts[np.argmin(sum_of_pts)]
    rect[2] = pts[np.argmax(sum_of_pts)]

    diff_of_pts = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff_of_pts)]
    rect[3] = pts[np.argmax(diff_of_pts)]

    return rect

def four_point_transform(image, pts):
    """
    image is also a numpy array of the image

    pts is a numpy array of image coords
    """

    rect = order_points(pts)
    (top_left, top_right, bottom_right, bottom_left) = rect

    #distance formula
    width_a = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) +\
    ((bottom_right[1] - bottom_left[1]) ** 2))
    width_b = np.sqrt(((top_right[0] - top_left[0]) ** 2) +\
    ((top_right[1] - top_left[1]) ** 2))
    max_width = max(int(width_a), int(width_b))

    height_a = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) +\
    ((top_right[1] - bottom_right[1]) ** 2))
    height_b = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) +\
    ((top_left[1] - bottom_left[1]) ** 2))
    max_height = max(int(height_a), int(height_b))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    perspective_transform_matrix = cv2.getPerspectiveTransform(rect, dst)
    warped_image = cv2.warpPerspective(image, perspective_transform_matrix,\
                                       (max_width, max_height))
    return warped_image

if __name__ == "__main__" : 
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--image", help="path to the image file")
    arg_parser.add_argument("-c", "--coords", \
                    help="comma separated list of source points")
    args = vars(arg_parser.parse_args())

    image = cv2.imread(args["image"])
    pts = np.array(eval(args["coords"]), dtype="float32")

    warped_image = four_point_transform(image, pts)

    cv2.imwrite('warped/' + args["image"], warped_image)
