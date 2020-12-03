import numpy as np
import Global

import os.path
import numpy as np

c_stahl = 5_850
c_water = 1_500

def calculate_forerun(angle):
    distance = Global.config["distance"]
    phi = np.arcsin((c_water/c_stahl) * np.cos(angle))
    return distance / np.cos(phi)

def calculate_first_way(height, angle):
    return height / np.sin(angle)

def calculate_time(way):
    return way / c_stahl

def calculate_time_water(way):
    return way / c_water

def calculate_distance_first_point_to_last(height, angle):
    #return 2 * height / np.tan(angle)
    return 2 * height / np.tan(angle)

def calculate_complete_distance(height, angle):
    first = calculate_distance_first_point_to_last(height, angle)
    second = height * np.tan(angle)
    return first + second

def calculate_way(time):
    return c_stahl * time

def calculate_normal_time(x, y, angle, height):
    forerun = 2 * calculate_forerun(angle)
    first_way = 2 * calculate_first_way(height, angle)

    #print(forerun, first_way)
    #print(calculate_distance_first_point_to_last(height, angle), x * Global.config["interval"])

    #dist = calculate_distance_first_point_to_last(height, angle) - x * Global.config["interval"] * (1/1000)
    #!wrong
    dist = calculate_complete_distance(height, angle) - x * Global.config["interval"] * (1/1000) - height / np.tan(angle)
    #print(dist)

    second_way = 2 * dist * np.cos(angle)

    #print(second_way)

    complete_way = forerun + first_way + second_way
    time = calculate_time(complete_way)

    #print(complete_way, time)

    return time

def find_mistakes_along_x_axis(y, length_of_picture=None, first=True, second=True, third=False, perc=100):

    height = Global.config["height"]
    angle_dec = Global.config["angle"]
    angle = np.pi * (angle_dec/180)

    height_real = height * 0.001

    first_way = calculate_first_way(height_real, angle)
    forerun = calculate_forerun(angle)

    first_way_time = calculate_time(first_way)
    forerun_time = calculate_time_water(forerun)

    sample = (4 * first_way_time + 2 * forerun_time) / Global.config["ybounds"]

    #mind_time_real = 2 * (first_way_time + forerun_time)
    mind_time_real = first_way_time + forerun_time

    mind_time = int(mind_time_real / sample)

    #print(mind_time)
    #!save bis hierhin

    complete_dist = calculate_complete_distance(height, angle)

    if length_of_picture:
        distance_difference = complete_dist - length_of_picture
    else:
        distance_difference = 0

    polygons = []

    #-------------Grenzen-----------------#
    area = 40
    area2 = 80

    #perc = perc/1000

    mind_time2 = mind_time*2

    #-----------------Algorithmus-------------------#
    for x in range(int(Global.config["scans"])):

        test_time = calculate_normal_time(x, y, angle, height_real)
        #print("border", test_time / sample)
        border = (test_time / sample)

        #border1 = border + area
        #border2 = border + area2

        #perc = 1 - perc

        border1 = border * (perc)
        border2 = border * (2 - perc)

        print(border, border1, border2)

        for i in range(mind_time, int(Global.config["ybounds"])):
        #for i in range(int(test_time/sample)-20, int(test_time/sample)+20):

            if(Global.array[y, x, i] <= 500):
                continue

            rad = 0.1 * (Global.array[y, x, i] / 1020)

            dist = calculate_complete_distance(height_real, angle) - x * Global.config["interval"] * (1/1000)
            #print(dist)

            second_dist = dist - (height_real / np.tan(angle))
            #second_way = 2 * second_dist * np.cos(angle)
            second_way = second_dist * np.cos(angle)


            if (first or third) and i < border1:
                if third:
                    continue
                #!Anwendung des Sinussatz
                #print("here", x)
                rest_time = (i - mind_time) * sample
                rest_way = calculate_way(rest_time)

                best = float('inf')
                best_b = 0
                best_omega = 0

               #print(rest_way)

                for omega in range(1, 90):
                    #print("new", omega)

                    omega *= (np.pi/180)
                    k = first_way / np.sin(omega)

                    gamma = np.pi - 2*angle
                    epsilon = 2*angle - omega

                   # print(omega, gamma, epsilon)

                    a = k * np.sin(gamma)
                    b = k * np.sin(epsilon)

                    #print(a, b)

                    if abs(rest_way - (a+b)) < best and a+b <= rest_way and b < second_way:
                        best = abs(rest_way - (a+b))
                        best_b = b
                        best_omega = omega

                way = best_b * 1000 + rad
                #print(best_b, best, best_omega)

            elif (second or third) and i > border2:
                if third:
                    continue

                rest_time = (i - mind_time) * sample
                rest_way = calculate_way(rest_time)

                #print(rest_time, rest_way)

                #dist = calculate_distance_first_point_to_last(height_real, angle) - x * Global.config["interval"] * (1/1000)
                #!Wrong

                best = float('inf')
                best_b = 0
                best_omega = 0

                #print("new", second_dist, dist, x)

                #print(rest_way)

                for omega in range(int(angle_dec), 90):
                    omega *= (np.pi/180)

                    way_part = height_real / np.sin(omega)
                    width = height_real / np.tan(omega)

                    #print(way_part, width)
                    """
                    for k in range(1, 10):
                        #r = (dist - k*width) / np.cos(omega)
                        anglebzh = (np.sin(omega)/np.tan((np.pi/2)-angle)) + np.cos(omega)
                        r = (dist - k*width) / anglebzh
                        if (r > 0):
                            new_way = k*way_part + r * (1 + (np.sin(omega)/np.sin(angle)))
                            if abs(rest_way - new_way) < best:
                                best = abs(rest_way - new_way)
                                best_b = r * (np.sin(omega)/np.sin(angle))
                                besti = [k, r, omega, new_way, way_part]
                    """
                    beginn = 0.001
                    for percentage in range(700, 1000):

                        per = beginn * percentage
                        r = per * second_way
                        rest = (1-per) * second_way

                        oomega = (np.pi/2) - omega
                        phi = np.pi - angle - oomega

                        weg = (r / np.sin(oomega)) * np.sin(phi)
                        rest_dist = second_dist - weg

                        k = int((dist - rest_dist) / width)
                        new_way = k * way_part + r * (1 + (np.sin(omega) / np.sin(angle)))


                        if k <= 10 and abs(rest_way - new_way) < best:
                            best = abs(rest_way - new_way)
                            best_b = r
                            besti = [k, r, omega, new_way, way_part]


                
                way = best_b * 1000 + rad

                #print(besti, best_b, rest_way)

            else:
                #print("g")
                #continue

                time = (i - mind_time2) * sample / 2
                way = calculate_way(time) * 1000 + rad

                #way = 0#!tetetetetetet

            #if way > 0:

            y_cord = way * np.sin(angle)
            x_cord = x * Global.config["interval"] + (height/np.tan(angle)) + way * np.cos(angle) - distance_difference

            polygons.append([x_cord, y_cord, rad])
        #break

    filename = Global.path + "/error{}.npy".format(y)

    if not os.path.isfile(filename):
        array = np.array(polygons)
        np.save(filename, array)

    return polygons
