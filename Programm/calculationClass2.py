import numpy as np

import Global

c_stahl = 5_850
c_water = 1_500

def calculate_forerun(angle):
    #distance = 0.02
    distance = Global.config["distance"]
    phi = np.arcsin((c_water/c_stahl) * np.cos(angle))
    #return 0
    return distance / np.cos(phi)

def calculate_first_way(height, angle):
    return height / np.sin(angle)

def calculate_complete_way(height, angle):
    return 4 * calculate_first_way(height, angle)

def calculate_distance_first_point_to_last(height, angle):
    return 2 * height / np.tan(angle)

def calculate_complete_distance(height, angle):
    first = calculate_distance_first_point_to_last(height, angle)
    second = height * np.tan(angle)
    return first + second

def calculate_time(way):
    return way / c_stahl

def calculate_time_water(way):
    return way / c_water

def calculate_way(time):
    return c_stahl * time

def find_mistakes_along_x_axis(y, length_of_picture=None):

    height = Global.config["height"]
    angle = Global.config["angle"]
    angle = np.pi * (angle/180)

    height_real = height * 0.001

    first_way = calculate_first_way(height_real, angle)
    forerun = calculate_forerun(angle)

    first_way_time = calculate_time(first_way)
    forerun_time = calculate_time_water(forerun)

    #complete_way = 4 * first_way
    sample = (4 * first_way_time + 2 * forerun_time) / Global.config["ybounds"]

    #!Wrong
    #sample = (14 / 1024) * 0.000000001

    mind_time_real = 2 * (first_way_time + forerun_time)

    mind_time = int(mind_time_real / sample)

    complete_dist = calculate_complete_distance(height, angle)

    if length_of_picture:
        distance_difference = complete_dist - length_of_picture
    else:
        distance_difference = 0

    polygons = []

    #print(height)
    #print(first_way, forerun)
    #print(first_way_time, forerun_time)
    #print(sample, mind_time)
    #print(complete_dist)
    #print(mind_time_real)
    #print(distance_difference)

    #print(Global.config)

    for x in range(int(Global.config["scans"])):
        #x = 80

        for i in range(mind_time, int(Global.config["ybounds"])):

            if(Global.array[y, x, i] > 500):

                rad = 0.1 * (Global.array[y, x, i] / 1020)

                time = (i - mind_time) * sample / 2
                way = calculate_way(time) * 1000 + rad

                y_cord = way * np.sin(angle)
                x_cord = x * Global.config["interval"] + (height/np.tan(angle)) + way * np.cos(angle) - distance_difference

                #print(time, mind_time)
                #print(way)
                #print(y_cord)
                #print(x*Global.config["interval"])
                #print(height/np.tan(angle))
                #print(way * np.cos(angle))

                polygons.append([x_cord, y_cord, rad])

                #break
        #break

    return polygons



#Global.changePath("test2")
#find_mistakes_along_x_axis(0)



