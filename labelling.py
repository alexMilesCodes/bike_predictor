import requests as rs
import numpy as np
import cv2


# define a function that takes in:
#    link - for the profile photo
#    distance
#    vert_meters (default none if not provided)
# ...and returns a list of altitudes (per every 100m? Every 500m?)
def label_profile(link, finish=False):
    # the image to display:
    image = cv2.imdecode(np.asarray(bytearray(rs.get(link, stream=True).raw.read()), dtype="uint8"), cv2.IMREAD_COLOR)
    # grayscale image to process:
    gs = cv2.imdecode(np.asarray(bytearray(rs.get(link, stream=True).raw.read()), dtype="uint8"), cv2.IMREAD_GRAYSCALE)
    # add reference points
    ref_x = []
    ref_alt = {}
    ref_y = {}
    add_point = True
    while add_point:
        cv2.imshow('Add Reference Point (press any key once selected)', image)
        cv2.setMouseCallback('Add Reference Point (press any key once selected)', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        alt = num_in('altitude of the reference point (in meters): ')
        ref_x.append(x)
        ref_alt[x] = alt
        ref_y[x] = y
        if len(ref_x) > 1:
            if input('enter 0 if done: ') == '0':
                add_point = False
    # trim for profile
    image = image[:, min(ref_x):max(ref_x), :]
    gs = gs[:, min(ref_x):max(ref_x)]
    # cv2.imshow('Add Top Boarder for trimming (press any key once selected)', image)
    # cv2.setMouseCallback('Add Top Boarder for trimming (press any key once selected)', click_event)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # image = image[y:, :, :]
    # gs = gs[y:, :]
    cv2.imshow('Add Bottom Boarder for trimming (press any key once selected)', image)
    cv2.setMouseCallback('Add Bottom Boarder for trimming (press any key once selected)', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    image = image[:y, :, :]
    gs = gs[:y, :]
    bot = y
    # CODE THAT REORDERS AND TRANSFORMS THE REFERENCE POINTS ACCORDING TO TRIMMING
    # ref_x.sort()
    # min_x = min(ref_x.copy())
    # for i in range(len(ref_x)):
    #     ref_y[ref_x[i]] -= ref_y[min_x]
    #     ref_alt[ref_x[i]] -= ref_alt[min_x]
    #     ref_x[i] -= min_x

    # IMAGE PROCESSING:
    print('calculating profile')
    rol_ave = np.zeros((gs.shape[1], gs.shape[0] - 2), dtype=int)
    alt_pix = np.zeros(gs.shape[1], dtype=int)
    for i in range(0, gs.shape[1]):
        for j in range(0, gs.shape[0] - 2):
            rol_ave[i, j] = np.average(gs[gs.shape[0] - j - 2:gs.shape[0] - j, i])
            if j > 2:
                if (rol_ave[i, j] - rol_ave[i, j - 3]) > 12 and alt_pix[i] == 0:
                    alt_pix[i] = j - 1

    # LOGIC TO AVOID GREY LINE ERROR
                    if gs[gs.shape[0] - 1, i] > 96 or i > gs.shape[1] - 3 or i < 2:
                        alt_pix[i] = j - 1
                    else:
                        alt_pix[i] = -1

    # IN CASE FINISH REPAIR LOGIC IS NEEDED
    # if finish:
    #     for i in range(int((image.shape[1] - 1) * 0.8)-3, int((image.shape[1] - 1) * 0.8)+4):
    #         alt_pix[i] = alt_pix[int((image.shape[1] - 1)*0.8)-4] + int(((i - (int((image.shape[1] - 1) * 0.8)-3)) /
    #                                                                      6) *
    #                                                                     (alt_pix[int((image.shape[1] - 1) * 0.8)+4] -
    #                                                                     alt_pix[int((image.shape[1] - 1) * 0.8)-4]))

    # replace -1 values
    for i in range(len(alt_pix)):
        if alt_pix[i] == -1:
            count = 1
            while alt_pix[i+count] == -1:
                count += 1
            for j in range(count):
                alt_pix[i+j] = int(round(alt_pix[i-1]+((j+1)/(count+1))*(alt_pix[i+count]-alt_pix[i-1]), 0))
    for i in range(0, gs.shape[1]):
        image[image.shape[0] - 2 - alt_pix[i], i, :] = [0, 0, 255]

    # define scaling factor
    scaling = 0.0
    temp = ref_x.copy()
    for i in range(len(ref_x)):
        if ref_y[ref_x[i]] == ref_y[max(ref_x)]:
            temp.remove(ref_x[i])
    for i in range(len(temp)):
        scaling = (scaling * i - (
                (ref_alt[temp[i]] - ref_alt[max(ref_x)]) / (ref_y[temp[i]] - ref_y[max(ref_x)]))) / (i + 1)

    # apply scaling
    alt = []
    for i in range(len(alt_pix)):
        alt.append(ref_alt[max(ref_x)] + scaling * (alt_pix[i] - alt_pix[len(alt_pix)-1]))

    cv2.imshow('Profile (press any key to exit)', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    rem = input('enter 0 if there are spikes to remove: ') == '0'

    # allow removal of spikes
    while rem:
        cv2.imshow('Click on the spike to remove (press any key once selected)', image)
        cv2.setMouseCallback('Click on the spike to remove (press any key once selected)', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if 2 < x < len(alt)-3:
            for i in [-1, 0, 1]:
                alt[x+i] = ((alt[x-2]+alt[x+2])/2) + 0.25*i*(alt[x+2]-alt[x-2])
                alt_pix[x+i] = ((alt_pix[x-2]+alt_pix[x+2])/2) + 0.25*i*(alt_pix[x+2]-alt_pix[x-2])
            image = cv2.imdecode(np.asarray(bytearray(rs.get(link, stream=True).raw.read()), dtype="uint8"),
                                 cv2.IMREAD_COLOR)
            image = image[:bot, min(ref_x):max(ref_x), :]
            for i in range(0, gs.shape[1]):
                image[image.shape[0] - 2 - alt_pix[i], i, :] = [0, 0, 255]
            print('removed')
        cv2.imshow('Profile (press any key to exit)', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        rem = input('enter 0 if there are spikes to remove: ') == '0'

    return alt


# function to change the global coordinates
# of the points clicked on the image
def click_event(event, x_click, y_click, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global x, y
        x = x_click
        y = y_click


def num_in(name):
    output = ''
    while output == '':
        temp = input(f'enter {name}: ')
        if not temp.isdigit():
            print('input must be a number')
        else:
            output = int(temp)
    return output
