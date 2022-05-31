# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries

import numpy as np
import cmath

class Dft:
    def __init__(self):
        pass

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""

        tempMatrix = np.zeros((15,15), dtype=complex)

        for u in range(15):
            for v in range(15):
                temp_num = 0
                for i in range(15):
                    for j in range(15):
                        temp_num += matrix[i][j] * cmath.exp(-1j*((2*np.pi)/15)*((u*i)+(v*j)))
                tempMatrix[u][v] = temp_num

        return tempMatrix

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse fourier transform"""

        tempMatrix = np.zeros((15,15), dtype=complex)

        for u in range(15):
            for v in range(15):
                temp_num = 0
                for i in range(15):
                    for j in range(15):
                        temp_num += matrix[i][j] * cmath.exp(1j*((2*np.pi)/15)*((u*i)+(v*j)))
                tempMatrix[u][v] = temp_num

        return tempMatrix

    def magnitude(self, matrix):
        """Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the complex matrix"""

        tempMatrix = np.zeros((15,15), dtype=complex)

        for u in range(15):
            for v in range(15):
                #squaring to get rid of the negative then square root to get original number
                temp = matrix[u][v]**2
                tempMatrix[u][v] = cmath.sqrt(temp)

        return tempMatrix