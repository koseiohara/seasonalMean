import numpy as np
import os
import warnings


class filein:

    def __init__(self, filename, shape, recl, rec, kind, endian, recstep):

        self.__argcheck(filename, shape, recl, rec, kind, recstep)

        #self.__file = file
        self.__filename = filename
        self.__shape = shape
        self.__recl = recl
        self.rec = rec
        self.__recstep = recstep

        self.__kind = self.get_kind(kind)
        self.__endian = self.get_endian(endian)

        self.__file = open(filename, 'rb')


    def __del__(self):
        if (not self.__file.closed):
            self.fclose()


    def fclose(self):
        self.__file.close()
        

    def fread(self):
        output = self.read_direct(self.__file, self.__shape, self.__recl, self.rec, self.__kind, self.__endian)

        if (np.any(np.isnan(output))):
            print('')
            print('Warning from fread : NaN is detected in input')
            print('    filename : {}'.format(self.__filename))
            print('    Record   : {}'.format(self.rec))
            print('')

        self.rec = self.rec + self.__recstep

        return output


    def read_direct(self, file, shape, recl, rec, kind, endian):

        if (file.closed):
            raise Exception('file has already been closed')


        if (rec <= 0):
            raise ValueError('rec must be more than zero, but input is {}'.format(rec))


        shape = np.array(shape)

        #kind_specifier   = self.get_kind(kind)
        #endian_specifier = self.get_endian(endian)

        #argcheck(file, shape, recl, rec, kind)

        skip_byte = recl * (rec-1)
        file.seek(skip_byte, os.SEEK_SET)
        input_binary = file.read(recl)

        return np.reshape(np.frombuffer(input_binary, \
                                        dtype='{}{}'.format(endian, kind)), \
                                        shape)


    def get_kind(self, kind):

        if (kind == 4):
            return 'f'
        elif (kind == 8):
            return 'd'
        else:
            raise ValueError('kind argument must be 4 or 8, but input is {}'.format(kind))


    def get_endian(self, endian):

        lower_endian = endian.lower()
        
        if (lower_endian == 'little'):
            return '<'
        elif (lower_endian == 'big'):
            return '>'
        else:
            raise ValueError('endian argument must be "little" or "big", but input is {}'.format(endian))


    def __argcheck(self, filename, shape, recl, rec, kind, recstep):

        if (type(filename) is not str):
            raise TypeError('filename must be a string variable')


        if (type(recl) is not int):
            raise TypeError('recl must be an integer, but input is {}'.format(type(recl)))


        if (type(rec) is not int):
            raise TypeError('rec must be an integer variable, but input is {}'.format(type(rec)))


        if (np.prod(shape)*kind != recl):
            print('')
            print('   shape, recl, and kind arguments do not match each other')
            print('   The product of shape and kind must be equal to recl')
            print('')

            raise ValueError('Data size of outputted array must same as the recl value')


        if (type(recstep) is not int):
            raise TypeError('recstep must be an integer variable, but input is {}'.format(type(recstep)))


        if (recstep <= 0):
            raise ValueError('recstep must be more than zero, but input is {}'.format(recstep))



