import math
import copy

# This class is for storing and operating on sudoku puzzles of arbitrary size (only 2-dimensional ones though).

# Matrix has to be in the form of:
# matrix = [[[value],[value], ...
# with one list of x columns and each column containing x lists with a maximum of one value in each.

class Sudoku:
    matrix = []
    __sudokusize__ = 0
    __sudokusubsize__ = 0


    def __init__(self, matrix):
        self.matrix = copy.deepcopy(matrix)
        self.__sudokusize__ = len(self.matrix)
        self.__sudokusubsize__ = math.sqrt(self.getSudokusize())

    # Method used to create a sudoku object, see above for formatting specifications of the matrix.
    @staticmethod
    def makeSudoku(matrix):
        return Sudoku(matrix)

    # Returns the length of one side of the sudoku
    def getSudokusize(self):
        return self.__sudokusize__

    # Returns the length of one side of one of the submatrices in the sudoku.
    def getSudokusubsize(self):
        return self.__sudokusubsize__

    # Returns all cells in the sudoku which only contain a single value.
    def getSingleValues(self):
        singlevalues = []
        for column in self.matrix:
            for value in column:
                if len(value) == 1:
                    singlevalues.append(value)
        return singlevalues

    # Returns a new matrix that keeps the references to the original cells.
    @staticmethod
    def matrixCopy(sudoku):
        tempmatrix = []
        for column in sudoku.getMatrix():
            tempmatrix.append([])
            for value in column:
                tempmatrix[-1].append(value)
        return tempmatrix

    # Returns the row indicated by the rowindex.
    def getRow(self, rowindex):
        row = []
        for column in self.matrix:
            row.append(column[rowindex])
        return row

    # Returns the column indicated by the columnindex.
    def getColumn(self, columnindex):
        return self.matrix[columnindex]

    # Returns the submatrix in which the cell indicated by the column- and row indices resides.
    def getSubMatrix(self, columnindex, rowindex):
        submatrix = []
        tempcolumnindex = int(columnindex * self.__sudokusubsize__)
        tempcolumnendindex = int(tempcolumnindex + self.__sudokusubsize__)
        temprowindex = int(rowindex * self.__sudokusubsize__)
        temprowendindex = int(temprowindex + self.__sudokusubsize__)

        while tempcolumnindex < tempcolumnendindex:
            submatrix.append(self.matrix[tempcolumnindex][temprowindex:  temprowendindex])
            tempcolumnindex += 1
        return submatrix

    # Returns a submatrix from a single index, the submatrices are numbered from 0 and up in standard western reading order (i.e. left -> right, and up -> down).
    def getSubMatrixFromSingleIndex(self, index):
        columnindex = int(index % self.__sudokusubsize__)
        rowindex = int(index / self.__sudokusubsize__)
        return self.getSubMatrix(columnindex, rowindex)

    # Returns an index in the format expected by the getSubMatrixFromSingleIndex() method from the indices of a single cell, such as the getSubMatrix() might expect.
    def getSubMatrixIndex(self, columnindex, rowindex):
        tempcolumnindex = int(columnindex / self.__sudokusubsize__)
        temprowindex = int(rowindex / self.__sudokusubsize__)
        submatrixindex = int(temprowindex * self.__sudokusubsize__ + tempcolumnindex % self.__sudokusubsize__)
        return submatrixindex

    def getSubmatrixForPruning(self, columnindex, rowindex):
        return self.getSubMatrixFromSingleIndex(self.getSubMatrixIndex(columnindex, rowindex))

    # Returns a list of all submatrices.
    def getSubMatrices(self):
        submatrices = []
        size = self.__sudokusize__
        while size:
            submatrices.append(self.getSubMatrixFromSingleIndex(size-1))
            size -= 1
        submatrices.reverse()
        return submatrices

    # Finds the column- and row indices of a specific cell by reference.
    def findIndex(self, value):
        for columnindex, column in enumerate(self.matrix):
            for rowindex, row in enumerate(column):
                if value is row:
                    return [columnindex, rowindex]

    # Returns the matrix.
    def getMatrix(self):
        return self.matrix

    # Sets the matrix.
    def setMatrix(self, matrix):
        self.matrix = matrix
        self.__sudokusize__ = len(self.matrix)
        self.__sudokusubsize__ = math.sqrt(self.getSudokusize())
