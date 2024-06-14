import numpy as np


def lat_def(latstep):
    lat = np.arange(90., -(90.+latstep), -latstep)
    lat[:] = lat[:] * np.pi /  180.

    return lat


def vint2gmean(vint, latstep, isYrev, range_south, range_north):
    lat = lat_def(latstep)
    nlat = lat.size

    PIHALF = np.pi * 0.5

    if (not isYrev):
        vint[:] = vint[::-1]

    for i in range(0, nlat):
        if (lat[i]-0.001 < range_north*np.pi/180.):
            firstIDX = i
            break
    for i in range(firstIDX, nlat):
        if (lat[i]-0.001 < range_south*np.pi/180.):
            lastIDX = i
            break


    #gmean = vint[0] * np.cos(lat[0]) * (PIHALF - lat[0]) * 0.25
    gmean = 0.

    for j in range(firstIDX, lastIDX):
        #print(lat[j]  *180./np.pi)
        #print(lat[j+1]*180./np.pi)
        gmean = gmean + (vint[j]*np.cos(lat[j]) + vint[j+1]*np.cos(lat[j+1])) * (lat[j] - lat[j+1]) * 0.25
    #gmean = gmean + vint[nlat-1] * np.cos(lat[nlat-1]) * (lat[nlat-1] + PIHALF) * 0.25

    return gmean

