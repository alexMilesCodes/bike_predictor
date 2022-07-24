import pandas as pd
import numpy as np
import requests as rs
import cv2
from labelling import click_event


old = pd.read_csv('profiles.csv')

for race in range(len(old['Link'])):

    i = 0
    alt = []
    while str(old[str(i)][race]) != 'nan':
        alt.append(old[str(i)][race])
        print(old[str(i)][race])
        i += 1

    x = 0
    y = 0
    image = cv2.imdecode(np.asarray(bytearray(rs.get(old['Link'][race], stream=True).raw.read()), dtype="uint8"),
                         cv2.IMREAD_COLOR)

    cv2.imshow('preview (press any key to exit)', image)
    cv2.setMouseCallback('preview (press any key to exit)', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    rem = input('enter s if there are spikes to remove: ') == 's'
    if rem:
        cv2.imshow('click on start (press any key to exit)', image)
        cv2.setMouseCallback('click on start (press any key to exit)', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        left_x = x
        cv2.imshow('click on finish (press any key to exit)', image)
        cv2.setMouseCallback('click on finish (press any key to exit)', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        right_x = x
        cv2.imshow('click on top (press any key to exit)', image)
        cv2.setMouseCallback('click on top (press any key to exit)', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        top_y = y
        cv2.imshow('click on bottom (press any key to exit)', image)
        cv2.setMouseCallback('click on bottom (press any key to exit)', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        bottom_y = y
    while rem:
        cv2.imshow('click on the spike to remove (press any key once selected)', image)
        cv2.setMouseCallback('click on the spike to remove (press any key once selected)', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if 2 < x < len(alt)-3:
            for i in [-1, 0, 1]:
                alt[x+i] = ((alt[x-2]+alt[x+2])/2) + 0.25*i*(alt[x+2]-alt[x-2])
            image = cv2.imdecode(np.asarray(bytearray(rs.get(old['Link'][race], stream=True).raw.read()),
                                            dtype="uint8"), cv2.IMREAD_COLOR)[top_y:bottom_y, left_x:right_x, :]

            for i in range(0, image.shape[1]):
                temp = int(round((alt[i]-min(alt))*(image.shape[0])/(max(alt)-min(alt)), 0))
                if temp < 0 or temp >= image.shape[0]:
                    image[temp, i, :] = [0, 0, 255]
            print('removed')
        cv2.imshow('profile (press any key to exit)', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        rem = input('enter s if there are spikes to remove: ') == 's'

