import numpy as np
import sys


def reader():
    file = sys.argv[1]
    input = np.loadtxt(file, delimiter=' ', dtype='str', skiprows=2)
    days = input[:,8]
    for m in range(12):
        days[m] = days[m][:-1]

    days = np.float64(days[:])
    clim = np.float64(input[:,-1])

    days_out = np.zeros(13)
    clim_out = np.zeros(13)

    days_out[1:] = days[:]
    clim_out[1:] = clim[:]

    #print(days)
    #print(clim)

    return days_out, clim_out


def seasonal():
    days, clim = reader()
    sum = days * clim

    DJF = (sum[1] + sum[2]  + sum[12]) / (days[1] + days[2]  + days[12])
    MAM = (sum[3] + sum[4]  + sum[5] ) / (days[3] + days[4]  + days[5] )
    JJA = (sum[6] + sum[7]  + sum[8] ) / (days[6] + days[7]  + days[8] )
    SON = (sum[9] + sum[10] + sum[11]) / (days[9] + days[10] + days[11])

    print('DJF : {:.5e}'.format(DJF))
    print('MAM : {:.5e}'.format(MAM))
    print('JJA : {:.5e}'.format(JJA))
    print('SON : {:.5e}'.format(SON))


seasonal()

