import code
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image

# code.interact(local=dict(globals(), **locals()))

image_name = 'sample_pics/test_6.png'
im = cv2.imread(image_name)
im_gray = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

(thresh, im_bw) = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

def segment_image(image):
    # Getting size of the image
    row_length = len(image)
    column_length = len(image[0])
    counter = 0
    boundaries = [[0,0,0,0]]
    for j in range(row_length):
        for i in range(column_length):
            if image[j][i] == 0:
                if check_within_boundary(boundaries,j,i):
                    continue
                else:
                    vertical_boundary = get_vertical_boundaries(image,j,i)
                    horizontal_boundary = get_horizontal_boundaries(image,j,i)
                    up = vertical_boundary[0]
                    down = vertical_boundary[1]
                    left = horizontal_boundary[0]
                    right = horizontal_boundary[1]
                    # code.interact(local=dict(globals(), **locals()))
                    boundaries.append([up,down,left,right])
    image_counter = 0
    for b in boundaries[1:len(boundaries)-1]:
        image_counter += 1
        cell_pic = im[b[0]:b[1] , b[2]:b[3]]
        diff_x = b[3] - b[2]
        diff_y = b[1] - b[0]
        try:
            ratio = diff_y / float(diff_x)
        except:
            continue
        # if ratio > 1.2 or ratio < 0.8:
        #     continue
        image_name = "Demo_segmentation/img_{}.png".format(image_counter)
        try:
            pic = Image.fromarray(cell_pic)
            pic.save(image_name)
        except:
            continue

def check_within_boundary(boundaries, row, column):
    in_boundary = False
    for i in range(len(boundaries)):
        up = boundaries[i][0]
        down = boundaries[i][1]
        left= boundaries[i][2]
        right = boundaries[i][3]
        # code.interact(local=dict(globals(), **locals()))
        if (up<=row<=down) and (left<=column<=right):
            in_boundary = True
            break
    return in_boundary

def get_horizontal_boundaries(image,row, column):
    row_length = len(image)
    column_length = len(image[0])
    i_right = column
    j_right = row
    i_left = column
    j_left = row
    horizontal_boundary_right = column
    horizontal_boundary_left = column
    image_test = image
    image_test_2 = image
    flag = 0
    # getting column boundaries (right side)
    while True:
        try:
            if image[j_right][i_right + 1] == 0:
                i_right += 1
                if horizontal_boundary_right < i_right:
                    horizontal_boundary_right = i_right
                flag = 1
            elif image[j_right + 1][i_right] == 0:
                j_right += 1
                flag = 0
            elif image[j_right][i_right - 1] == 0 and flag != 1:
                i_right -= 1
                flag = 2
            else:
                break
            # image[j_right][i_right] == 220
        except:
            break


    flag = 0
    # getting column boundaries (left side)
    while True:
        try:
            if image[j_left][i_left - 1] == 0:
                i_left -= 1
                if horizontal_boundary_left > i_left:
                    horizontal_boundary_left = i_left
                flag = 1
            elif image[j_left + 1][i_left] == 0:
                j_left += 1
                flag = 0
            elif image[j_left][i_left + 1] == 0 and flag !=1:
                i_left += 1
                flag = 2
            else:
                break
        except:
            break

    # plt.imshow(image)
    # plt.show()
    return [horizontal_boundary_left, horizontal_boundary_right]

def get_vertical_boundaries(image,row, column):
    row_length = len(image)
    column_length = len(image[0])
    vertical_boundary_down = row
    vertical_boundary_up = row
    j_down = row
    i_down = column
    image_test_3 = image
    flag = 0
    # Getting the lower boundaries
    while True:
        try:
            if image[j_down+1][i_down] == 0:
                j_down += 1
                vertical_boundary_down = j_down
                flag = 0
            elif image[j_down+1][i_down+1] == 0:
                i_down += 1
                j_down += 1
                vertical_boundary_down = j_down
                flag = 0
            elif image[j_down+1][i_down-1] == 0:
                j_down += 1
                i_down -= 1
                vertical_boundary_down = j_down
                flag = 0
            elif image[j_down][i_down+1] == 0 and flag != 2:
                i_down +=1
                flag = 1
            elif image[j_down][i_down-1] == 0 and flag !=1:
                i_down -= 1
                flag = 2
            else:
                break
        except:
            break
    return [vertical_boundary_up, vertical_boundary_down]

segment_image(im_bw)
