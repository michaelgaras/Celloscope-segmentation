import code
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image

# code.interact(local=dict(globals(), **locals()))

image_name = 'Demo_test_3.png'
im = cv2.imread(image_name)

im_gray = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

(thresh, im_bw) = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# code.interact(local=dict(globals(), **locals()))

def segment_image(image):
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
                    if counter == 0:
                        vertical_boundary = get_vertical_boundaries(image,j,i)
                        horizontal_boundary = get_horizontal_boundaries(image,j,i)
                        up = vertical_boundary[0]
                        down_1 = vertical_boundary[1]
                        down_2 = horizontal_boundary[2]
                        down_3 = horizontal_boundary[3]
                        lowest_pixel = [down_1, down_2,down_3]
                        down = max(lowest_pixel)
                        left = horizontal_boundary[0]
                        right = horizontal_boundary[1]
                        # code.interact(local=dict(globals(), **locals()))
                        boundaries.append([up,down,left,right])
                        counter = counter + 1

    image_counter = 0
    # for b in boundaries[0:len(boundaries)-1]:
    image_counter += 1
    code.interact(local=dict(globals(), **locals()))
    cell_pic = im[boundaries[1][0]:boundaries[1][1] , boundaries[1][2]:boundaries[1][3]]
    # diff_x = b[3] - b[2]
    # diff_y = b[1] - b[0]
    # try:
    #     ratio = diff_y / float(diff_x)
    # except:
    #     continue
    image_name = "testing/img_testing.png".format(image_counter)
    # try:
    pic = Image.fromarray(cell_pic)
    pic.save(image_name)
        # except:
        #     continue

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

def get_horizontal_boundaries(sample_image,row, column):
    row_length = len(sample_image)
    column_length = len(sample_image[0])
    i_right = column
    j_right = row
    i_left = column
    j_left = row
    horizontal_boundary_right = column
    horizontal_boundary_left = column
    image_test = sample_image
    image_test_2 = sample_image
    flag = 0
    # getting column boundaries (right side)
    while True:
        try:
            if sample_image[j_right][i_right + 1] != 255 and flag !=2:
                i_right += 1
                if horizontal_boundary_right < i_right:
                    horizontal_boundary_right = i_right
                flag = 1
                # print "here1"
            elif sample_image[j_right + 1][i_right] != 255:
                j_right += 1
                flag = 0
                # print "here2"
            elif sample_image[j_right][i_right - 1] != 255:
                i_right -= 1
                flag = 2
                # print "here3"
            else:
                break
            image_test[j_right][i_right] = 150
        except:
            break


    flag = 0
    # getting column boundaries (left side)
    while True:
        try:
            if sample_image[j_left][i_left - 1] != 255 and flag != 2:
                i_left -= 1
                if horizontal_boundary_left > i_left:
                    horizontal_boundary_left = i_left
                flag = 1
            elif sample_image[j_left + 1][i_left] != 255:
                j_left += 1
                flag = 0
            elif sample_image[j_left][i_left + 1] != 255:
                i_left += 1
                flag = 2
            else:
                break
            image_test[j_left][i_left] = 100
        except:
            break
    plt.imshow(image_test)
    plt.show()
    return [horizontal_boundary_left, horizontal_boundary_right, row, j_left, j_right] # row = top point, j_left = lowest pt on the left, j_right = lowest pt on the right

def get_vertical_boundaries(sample_image,row, column):
    row_length = len(sample_image)
    column_length = len(sample_image[0])
    vertical_boundary_down = row
    vertical_boundary_up = row
    j_down = row
    i_down = column
    image_test_3 = sample_image
    flag = 0
    # Getting the lower boundaries
    while True:
        try:
            if sample_image[j_down+1][i_down] != 255:
                j_down += 1
                vertical_boundary_down = j_down
                flag = 0
            elif sample_image[j_down+1][i_down+1] != 255:
                i_down += 1
                j_down += 1
                vertical_boundary_down = j_down
                flag = 0
            elif sample_image[j_down+1][i_down-1] != 255:
                j_down += 1
                i_down -= 1
                vertical_boundary_down = j_down
                flag = 0
            elif sample_image[j_down][i_down+1] != 255 and flag != 2:
                i_down +=1
                flag = 1
            elif sample_image[j_down][i_down-1] != 255 and flag !=1:
                i_down -= 1
                flag = 2
            else:
                break
            image_test_3[j_down][i_down] = 300
            # code.interact(local=dict(globals(), **locals()))
        except:
            break

    plt.imshow(image_test_3)
    plt.show()
    return [vertical_boundary_up, vertical_boundary_down]

segment_image(im_bw)
