import numpy as np
import datetime
from filein import filein as filein
from vint2gmean import vint2gmean as vint2gmean


def get_clim(input_fname, rec, varnum, nt):

    ny = 145
    recl = 4*ny

    vint_input = filein(input_fname, [ny], recl, 1, 4, 'LITTLE', 1)

    for t in range(nt):
        input = vint_input.fread()
        #vint[:] = vint[:] + vint_input.fread()
        vint[:] = vint[:] + input[:]

    vint[:] = vint[:] / np.float64(nt)

    return vint


def out_clim(input_fname, output_fname, dtype, varname):

    if (dtype == 'VINT'):
        ny = 145
    elif (dtype == 'GMEAN'):
        ny = 1

    recl = 4*ny
    vint_input = filein(input_fname, [ny], recl, 1, 4, 'LITTLE', 1)

    f = open(output_fname, 'w')
    f.write('INPUT FILE : {}\n'.format(input_fname))
    f.write('VARIABLE   : {}\n'.format(varname))

    hstep = 6
    date = datetime.datetime(2000, 1, 1, 0, 0)

    for m in range(1, 13):
        
        nhrs = 0

        vint = np.zeros(ny)
        month = int(datetime.datetime.strftime(date, '%m'))
        while (month == m):
            if (month == 2 and int(datetime.datetime.strftime(date, '%d')) == 29):
                date = date + datetime.timedelta(hours = hstep)
                month = int(datetime.datetime.strftime(date, '%m'))
                continue
           
            vint[:] = vint[:] + vint_input.fread()

            date = date + datetime.timedelta(hours = hstep)
            month = int(datetime.datetime.strftime(date, '%m'))
            nhrs = nhrs + 1

        vint[:] = vint[:] / np.float64(nhrs)

        if (dtype == 'VINT'):
            gmean = vint2gmean(vint, 1.25, True, -90., 90.)
        elif (dtype == 'GMEAN'):
            gmean = vint[0]

        f.write('MONTH : {:02d}, '.format(m))
        f.write('HOUR-NUM : {}, '.format(nhrs))
        f.write('DAY-NUM : {}, '.format(int(nhrs*hstep/24)))
        f.write('MONTHLY-MEAN : {:.3e}\n'.format(gmean))

    #f.write('NT : {}\n'.format(nt))
    #f.write('')
    #f.write('RESULT : {}\n'.format(gmean))
    f.close()



varname = 'qe'
dtype = 'VINT'
input_fname = '/mnt/jet11/kosei/mim/energetics/hourly_clim/output/JRA3Q_1980_2023_ALL_{}_{}.dat'.format(dtype, varname)
output_fname = './result/JRA3Q_1980_2023_{}_clim.txt'.format(varname)
out_clim(input_fname, output_fname, dtype, varname)

