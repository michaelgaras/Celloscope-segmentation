import code
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image
import os
import datetime
import random
import time
import matplotlib.patches as patches

# code.interact(local=dict(globals(), **locals()))
def segment_image(image, image_counter, directory):
    # Getting size of the image
    row_length = len(image)
    column_length = len(image[0])
    counter = 0
    boundaries = [[0,0,0,0]]
    for j in range(row_length):
        for i in range(column_length):
            if image[j][i] != 255:
                if check_within_boundary(boundaries,j,i):
                    continue
                else:
                    vertical_boundary = get_vertical_boundaries(image,j,i)
                    horizontal_boundary = get_horizontal_boundaries(image,j,i)
                    up = vertical_boundary[0]
                    left = horizontal_boundary[0]
                    right = horizontal_boundary[1]
                    down_1 = vertical_boundary[1]
                    down_2 = horizontal_boundary[2]
                    down_3 = horizontal_boundary[3]
                    lowest_pixel = [down_1, down_2,down_3]
                    down = max(lowest_pixel)
                    boundaries.append([up,down,left,right])
    image_counter = crop_cells(image, boundaries, image_counter, directory)
    draw_boundary(image, boundaries)
    return image_counter

def crop_cells(image, boundaries, image_counter, directory):
    row_length = len(image)
    column_length = len(image[0])
    for b in boundaries[1:len(boundaries)-1]:
        image_counter += 1
        # accounting for negative boundaries
        for j in range(len(b)):
            if b[j] < 0:
                b[j] = 1
        if b[3]> column_length:
            b[3] = column_length
        if b[1]> row_length:
            b[1] = row_length
        cell_pic = im[b[0]:b[1] , b[2]:b[3]]
        diff_x = b[3] - b[2]
        diff_y = b[1] - b[0]
        try:
            ratio = diff_y / float(diff_x)
        except:
            continue
        if ratio > 1.8 or ratio < 0.2:
            continue
        image_name = directory + "/image_{}.png".format(image_counter)
        try:
            pic = Image.fromarray(cell_pic)
            pic.save(image_name)
        except:
            image_counter -= 1
            continue
    return image_counter

def draw_boundary(picture, boundaries):
    for i in boundaries[1:len(boundaries)-1]:
        diff_x = i[3] - i[2]
        diff_y = i[1] - i[0]
        try:
            ratio = diff_y / float(diff_x)
        except:
            continue
        colour = random.randint(10, 170)
        cv2.rectangle(picture, (i[2], i[0]), (i[3], i[1]), (colour,0,0), 2)

    plt.imshow(picture)
    plt.show()

def check_within_boundary(boundaries, row, column):
    in_boundary = False
    for i in range(len(boundaries)):
        up = boundaries[i][0]
        down = boundaries[i][1]
        left= boundaries[i][2]
        right = boundaries[i][3]
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
            if image[j_right][i_right + 1] != 255 and flag !=2:
                i_right += 1
                if horizontal_boundary_right < i_right:
                    horizontal_boundary_right = i_right
                flag = 1
            elif image[j_right + 1][i_right] != 255:
                j_right += 1
                flag = 0
            elif image[j_right][i_right - 1] != 255:
                i_right -= 1
                flag = 2
            else:
                break
        except:
            break

    flag = 0
    # getting column boundaries (left side)
    while True:
        try:
            if image[j_left][i_left - 1] != 255 and flag != 2:
                i_left -= 1
                if horizontal_boundary_left > i_left:
                    horizontal_boundary_left = i_left
                flag = 1
            elif image[j_left + 1][i_left] != 255:
                j_left += 1
                flag = 0
            elif image[j_left][i_left + 1] != 255:
                i_left += 1
                flag = 2
            else:
                break
        except:
            break
    # returns row = top point, j_left = lowest pt on the left,
    # j_right = lowest pt on the right
    return [horizontal_boundary_left, horizontal_boundary_right, row, j_left, j_right]

def get_vertical_boundaries(image,row, column):
    row_length = len(image)
    column_length = len(image[0])
    vertical_boundary_down = row
    vertical_boundary_up = row
    j_down = row
    i_down = column
    j_up = row
    i_up = column
    image_test_3 = image
    flag = 0
    # Getting the lower boundaries
    while True:
        try:
            if image[j_down+1][i_down] != 255:
                j_down += 1
                vertical_boundary_down = j_down
                flag = 0
            elif image[j_down+1][i_down+1] != 255:
                i_down += 1
                j_down += 1
                vertical_boundary_down = j_down
                flag = 0
            elif image[j_down+1][i_down-1] != 255:
                j_down += 1
                i_down -= 1
                vertical_boundary_down = j_down
                flag = 0
            elif image[j_down][i_down+1] != 255 and flag != 2:
                i_down +=1
                flag = 1
            elif image[j_down][i_down-1] != 255 and flag != 1:
                i_down -= 1
                flag = 2
            else:
                break
        except:
            break

        # while True:
        #     try:
        #         if image[j_up-1][i_up] != 255:
        #             j_up -= 1
        #             vertical_boundary_up = j_up
        #             flag = 0
        #         elif image[j_up-1][i_up+1] != 255:
        #             i_up += 1
        #             j_up -= 1
        #             vertical_boundary_up = j_up
        #             flag = 0
        #         else:
        #             break
        #     except:
        #         break

    return [vertical_boundary_up, vertical_boundary_down]

image_counter = 1
currentDT = datetime.datetime.now()
time_stamp = str(currentDT).replace(':', '_').replace('.', '_')
directory = "Segmented_images/" + time_stamp
os.makedirs(directory)
# for k in range(1,2):
# image_name = 'sample_pics/normal_cells/rbc_{}.png'.format(k)
image_name = 'sample_pics/normal_cells/rbc_6.png'
print image_name
im = cv2.imread(image_name)
im_gray = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
# code.interact(local=dict(globals(), **locals()))
(thresh, im_bw) = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
image_counter = segment_image(im_bw, image_counter, directory)
