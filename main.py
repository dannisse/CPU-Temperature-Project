# Dannisse Arenas
# Semester Project
# Professor Kennedy
# CS 417
# 18 April 2022

import os
import re
import sys

file_name = sys.argv[1]
file_notxt = file_name.replace(".txt", "")

#data input module
def data_input(data):
    """
    Read and parse CPU temps text file

    Args:
        data: the .txt file
    Yields:
        A list containing an entry of floating point values.
    """
    for step, line in enumerate(data):
        yield [float(entry) for entry in line.split()]


def convert(file):
    """
    Take in an input file and converts the input file.

    Args:
        file: an input file
    Yields:
        Reads in file and replaces the data in the file with converted data that no longer contains labels.
        (Removes values like +°C as well as non- ASCII values i.e. Â)
    """
    with open(file_name, 'r+') as file:
        text = file.read()
        file.seek(0)
        new_text = remove_non_ascii(text)
        file.write(re.sub(r'[+°C]', '', new_text)) #source: https://pythonguides.com/remove-non-ascii-characters-python/#:~:text=Remove%20Non%2DASCII%20Characters%20From%20Text%20Python,-In%20this%20section&text=Here%20we%20can%20use%20the,a%20new%20or%20empty%20string.
        file.truncate() # get rid of trailing characters
        file.close()

#Source from lines 42-44:
#https://stackoverflow.com/questions/68184336/replace-line-in-file-using-re

def cores():
    """
        Removes labels if there are any in the provided input file and separates all four cores into seperate txt files.
     Yields:
        Creates files that will be used for core storage. While file is open, it converts the file to remove labels,
        and takes the split values from the lines of the file and tuples them to a list. It will also yield 4 core files
        that contains each cores CPU temperatures. The 4 core files are then closed.
     """
    with open(file_name) as file:
        convert(file)
        temps = [tuple(line.split()) for line in file]
    core_1 = open("core_1.txt", "a")
    core_2 = open("core_2.txt", "a")
    core_3 = open("core_3.txt", "a")
    core_4 = open("core_4.txt", "a")
    for row in temps:
        core_1.write(row[0] + "\n")
        core_2.write(row[1] + "\n")
        core_3.write(row[2] + "\n")
        core_4.write(row[3] + "\n")
    core_1.close()
    core_2.close()
    core_3.close()
    core_4.close()

#interpoolation module
def interpolation():
    """
        Does proper calculations and outputs interpolation for all CPU temperatures into a txt file.

       Yields:
          Calculates the interpolation and writes it into the file that will be used as final output.
       """
    for c in range(1, 5):
        core_num = str(c)
        core_file = str("core_" + core_num + ".txt")
        inter_file = str(file_notxt + "-core_" + core_num + ".txt")
        core = open(core_file, "r")
        temps = core.read().splitlines()
        inter = open(inter_file, "a")

        for i in range(len(temps) - 1):
            sec = int(i * 30)
            b = float(temps[i])
            xk1 = int((i + 1) * 30)
            d = float(temps[i + 1])
            c1 = ((d - b) / (xk1 - sec))
            c2 = b + (-sec * c1)
            inter.write(str(sec) + "<= x < " + str(xk1) + "; y_" + str(i) + " = " + str(c2) + " + " + str(c1) +
                        "x" + "; interpolation \n")
            i += 1
    core.close()
    inter.close()


# referenced mathematics in interpolation notes on
# https://www.cs.odu.edu/~tkennedy/cs417/latest/Directory/outline/index.html

#make table
def matrixX(data):
    """
       Takes the data set from the CPU temperatures and returns a list of each element.

       Args:
           data:a list of each CPU temps values with a time and a list of temps
       Yields:
           Matrix X as a nested list
       """
    xMatrix = []
    for i in range(len(data)):
        file = open(file_name, "r")
        temps = file.read().splitlines()
        sec = [i * 30 for i in range(len(temps))]
        xMatrix.append([1, sec[i]])
    return xMatrix


# based from https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/m


def matrixY(temps):
    """
           Take in an list that contains all of the CPU temperatures that were provided from the input file. Each index
           in this list contain one CPU temperature.

           Args:
               temps: list of CPU temperatures values, one per index in the list.
           Yields:
               Matrix Y in the form of a list to be used for least squares calculation.
           """
    yMatrix = []
    for i in range(len(temps)):
        xy = []
        x = float(temps[i])
        xy.append(x)
        yMatrix.append(xy)
    return yMatrix


# based from https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/

def transpose(x):
    """
     Take in list of time increment values.

     Args:
         x: an list that contains 30 second time increments. index one of x contains [1,30]
     Yields:
         transposed matrix, which will be used for the least squares calculation
     """
    # referenced from https://www.geeksforgeeks.org/transpose-matrix-single-line-python/
    # begin quote
    tMatrix = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
    # end quote
    return tMatrix

#least sq population module
def least_squares(data, temps, core_num):
    """
     Take in input data in the form of a list each index containing 4 CPU temperature values, list of temps that
     contain all of the temperature increments in the form of a list, and the number of cores that are being incremented
     in the main function as it goes through the loop.

     Args:
         data: list of 4 CPU temperatures values per index in the list.
         temps: an list that contains 30 second time increments. index one of x contains [1,30]
         core_num: the number of cores.
     Yields:
         Writes in the least squares approximation into the final output file after creating the X and Y matrices, and
         doing the appropriate matrix multiplication and transposing.

     """
    square_output = str(file_notxt + "-core-" + core_num + ".txt")
    square = open(square_output, "a")
    x = matrixX(data)
    y = matrixY(temps)
    xT = transpose(x)
    xTx = multiply(xT, x)
    xTy = multiply(xT, y)
    xtx_xty = []
    for i in range(len(xTx)):
        xtx_xty.append(xTx[i] + xTy[i])
        sec = int(i * 30)

    solved = gaussianElimination(xtx_xty)
    square.write(str(sec - 30) + " <= x < " + str((len(data) - 1) * 30) + ';   y = ' + str(abs(solved[0])) + " "
                 + str(solved[1]) + "x" + "; least-squares")
    square.close()


def multiply(m1, m2):
    """
       Takes in two matrices and preforms matrix multiplication on them.

       Args:
           m1: transposed matrix in the form of a list
           m2: matrix in the form of a list
       Yields:
            Returns the resulted matrix after doing matrix multiplication on the two inputted matrices.

       """

    result = [[0 for x in range(len(m2[0]))] for y in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                result[i][j] += m1[i][k] * m2[k][j]
    return result


#pseudocode from https://www.cs.odu.edu/~tkennedy/cs417/latest/Assts/matrixSolverExercise/index.html

def remove_non_ascii(s):
    """
        Takes in input file in the form of a string and removes all non ASCII characters.
         Args:
             s: a string of the input file.
         Yields:
              A converted string of the input file that no longer contains non-ASCII values like Â.

         """
    # referenced from
    # https://stackoverflow.com/questions/1342000/how-to-make-the-python-interpreter-correctly-handle-non-ascii-characters-in-stri
    return "".join(c for c in s if ord(c) < 128)

# referenced from
# https://stackoverflow.com/questions/1342000/how-to-make-the-python-interpreter-correctly-handle-non-ascii-characters-in-stri


def gaussianElimination(matrix):
    """
        Takes in matrix and calculates gaussian elimination/ row reduction on provided matrix.
         Args:
             matrix: a matrix in the form of a list.
         Yields:
              a row reduced matrix that will be used for the least squares calculation.

         """
    rows = len(matrix)

    for x in range(0, rows):
        max_s = abs(matrix[x][x])
        maxrows = x
        for y in range(x + 1, rows):
            if abs(matrix[y][x]) > max_s:
                max_s = abs(matrix[y][x])
                maxrows = y

        for y in range(x, rows + 1):
            result = matrix[maxrows][y]
            matrix[maxrows][y] = matrix[x][y]
            matrix[x][y] = result

        for y in range(x + 1, rows):
            result2 = -matrix[y][x] / matrix[x][x]
            for z in range(x, rows + 1):
                if x == z:
                    matrix[y][z] = 0
                else:
                    matrix[y][z] += result2 * matrix[x][z]

    result = [0 for i in range(rows)]
    # from https://rosettacode.org/wiki/Gaussian_elimination#Python begin quote:
    for x in range(rows - 1, -1, -1):
        result[x] = matrix[x][rows] / matrix[x][x]
        for y in range(x - 1, -1, -1):
            matrix[y][rows] -= matrix[y][x] * result[x]
        # end quote
    return result


# based functions from https://rosettacode.org/wiki/Gaussian_elimination#Python
# and https://www.cs.odu.edu/~tkennedy/cs417/latest/Assts/matrixSolverExercise/index.html

def main():
    """
        This function calls the appropriate functions, and works to run the program to provide the expected output. Will
        also delete the 4 temporary files that were used to store each core temperature.
         """
    cores()
    interpolation()

    data = []
    with open(file_name, 'r') as file:
        for i in data_input(file):
            data.append(i)

    for c in range(1, 5):
        core_num = str(c)
        core_file = str("core-" + core_num + ".txt")
        core = open(core_file, "r")
        temps = []
        temps = core.read().splitlines()
        least_squares(data, temps, core_num)
        core.close()

    for c in range(1, 5):
        core_num = str(c)
        core_file = str("core-" + core_num + ".txt")
        os.remove(core_file)


if __name__ == '__main__':
    main()
