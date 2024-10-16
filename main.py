import numpy as np
import datetime
from filein import filein as filein
from vint2gmean import vint2gmean as vint2gmean


def fill(vint):
    length = len(vint[:])
    output = np.empty(length)
    output[:] = vint[:]
    if (np.any(np.isnan(output[:]))):
        #print(output)
        #length   = len(output[:])
        left  = 0
        right = length
        for i in range (length):
            if (np.isnan(output[i])):
                if (i == 0 or i == length-1):
                    output[i] = 0.
                    continue

                for j in range (len(output[i+1:])):
                    right = j + i+1
                    distance = j + 2
                    if (not np.isnan(output[right])):
                        break
                #print('i-1 :', i-1)
                #print('right :', right)
                #print('distance :', distance)
                output[i] = output[i-1] - (output[i-1] - output[right])/distance

        #print(output)

    return output


def get_clim(input_fname, rec, varnum, nt):

    ny = 145
    recl = 4*ny

    vint_input = filein(input_fname, [ny], recl, 1, 4, 'LITTLE', 1)

    for t in range(nt):
        input = vint_input.fread()
        #vint[:] = vint[:] + vint_input.fread()

        fill(input)

        vint[:] = vint[:] + input[:]

    vint[:] = vint[:] / np.float64(nt)

    return vint


def out_clim(input_fname, output_fname, dtype, varname, south, north, leap):

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
    if (leap):
        date = datetime.datetime(2000, 1, 1, 0, 0)
    else:
        date = datetime.datetime(2001, 1, 1, 0, 0)

    for m in range(1, 13):
        
        nhrs = 0

        vint = np.zeros(ny)
        month = int(datetime.datetime.strftime(date, '%m'))
        while (month == m):
            if (month == 2 and int(datetime.datetime.strftime(date, '%d')) == 29):
                date = date + datetime.timedelta(hours = hstep)
                month = int(datetime.datetime.strftime(date, '%m'))
                continue

            input = vint_input.fread()

            input = fill(input)
           
            vint[:] = vint[:] + input

            date = date + datetime.timedelta(hours = hstep)
            month = int(datetime.datetime.strftime(date, '%m'))
            nhrs = nhrs + 1

        vint[:] = vint[:] / np.float64(nhrs)

        if (dtype == 'VINT'):
            gmean = vint2gmean(vint, 1.25, True, south, north)
        elif (dtype == 'GMEAN'):
            gmean = vint[0]

        f.write('MONTH : {:02d}, '.format(m))
        f.write('HOUR-NUM : {}, '.format(nhrs))
        f.write('DAY-NUM : {}, '.format(int(nhrs*hstep/24)))
        f.write('MONTHLY-MEAN : {:.5e}\n'.format(gmean))

    #f.write('NT : {}\n'.format(nt))
    #f.write('')
    #f.write('RESULT : {}\n'.format(gmean))
    f.close()


dataset = 'JRA55'
varname = 'qz'
dtype   = 'VINT'
flag    = ''
flag    = '_QFILTER'
start   = 1990
end     = 2020
leap    = False
#input_fname = '/mnt/jet11/kosei/mim/energetics/hourly_clim/output/JRA3Q_1980_2023_ALL_{}_{}_movave_2records_filter_forQ.dat'.format(dtype, varname)
input_fname = '../shift/output/{}/{}_{}_{}_ALL_{}_SHIFT_{}{}.grd'.format(dataset, dataset, start, end, dtype, varname, flag)
output_fname = './result/{}_{}_{}/{}_{}_{}_{}_clim{}.txt'.format(dataset, start, end, dataset, start, end, varname, flag)

print(input_fname)
print(output_fname)
out_clim(input_fname, output_fname, dtype, varname, -90., 90., leap)

