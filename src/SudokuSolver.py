import copy


# This program solves a valid sudoku puzzle; it can't solve them all so it'll return a sudoku object with an empty list as its matrix in case it fails to solve the sudoku. This way you can simply use the len() method on the matrix in the resulting sudoku object to see if it was succesfully solved.

class SudokuSolver:
    __paradox__ = False
    __tempsudoku__ = []
    __size__ = 0
    __checkedsinglevalues__ = []
    __uncheckedsinglevalues__ = []
    __allpossiblevalues__ = []
    __initsudoku__ = []

    def __init__(self, sudoku):
        self.__tempsudoku__ = copy.deepcopy(sudoku)  # Deepcopy of the input-sudoku to ensure that it is not inadvertantly changed.
        self.__size__ = self.__tempsudoku__.getSudokusize()
        self.__checkedsinglevalues__.extend(self.__tempsudoku__.getSingleValues())
        self.__uncheckedsinglevalues__ = []
        self.__allpossiblevalues__ = self.__generateAllPossibleValues__()
        self.plantEverything()
        self.__initsudoku__ = copy.deepcopy(self.__tempsudoku__)
        self.solve()

    # Use the following static method to solve a sudoku, all you have to do is to send it a sudoku object with the given values filled in.
    @staticmethod
    def actuallySolve(sudoku):
        return SudokuSolver(sudoku).__tempsudoku__

    # Checks to see if two cells in the same column/row/submatrix have the same value; sets_paradox if this is the case.
    def assistingValueCheck(self, value1, value2):
        if len(value1) == 1 and len(value2) == 1 and value1[0] == value2[0] and value1 is not value2:
            self.__paradox__ = True

    # Appends a cell to the list of unchecked single values if it has been pruned and left with a single value inside.
    def valueCheck(self, value1, value2):
        self.assistingValueCheck(value1, value2)
        if len(value2) == 1 and value2 not in self.__checkedsinglevalues__ and value2 not in self.__uncheckedsinglevalues__:
            self.__uncheckedsinglevalues__.append(value2)

    # Simply generates a list of all values that should be found in the sudoku.
    def __generateAllPossibleValues__(self):
        allpossiblevalues = []
        size = self.__tempsudoku__.getSudokusize()
        while size:
            allpossiblevalues.append(size)
            size -= 1
        allpossiblevalues.sort()
        return allpossiblevalues

    # Returns a list of all values that should be found in the sudoku.
    def getAllPossibleValues(self):
        return self.__allpossiblevalues__

    # In every empty cell all values which could possibly belong are added by this method.
    def plantEverything(self):
        tempmatrix = self.__tempsudoku__.getMatrix()
        columnvalues, rowvalues, submatrixvalues, = [], [], []

        for columnindex, column in enumerate(tempmatrix):
            valuesincolumn = []
            for value in column:
                if len(value) == 1:
                    valuesincolumn.append(value[0])
            columnvalues.append(valuesincolumn)

        for rowindex, column in enumerate(tempmatrix):
            valuesinrow = []
            for value in self.__tempsudoku__.getRow(rowindex):
                if len(value) == 1:
                    valuesinrow.append(value[0])
            rowvalues.append(valuesinrow)

        submatrices = self.__tempsudoku__.getSubMatrices()
        for submatrix in submatrices:
            valuesinsubmatrix = []
            for column in submatrix:
                for value in column:
                    if len(value) == 1:
                        valuesinsubmatrix.append(value[0])
            submatrixvalues.append(valuesinsubmatrix)

        for columnindex, column in enumerate(tempmatrix):
            for rowindex, row in enumerate(column):
                submatrixindex = self.__tempsudoku__.getSubMatrixIndex(columnindex, rowindex)
                if not len(row):
                    values = []
                    for value in self.getAllPossibleValues():
                        if value not in columnvalues[columnindex] and value not in rowvalues[rowindex] and value not in \
                                submatrixvalues[submatrixindex]:
                            values.append(value)
                    tempmatrix[columnindex][rowindex].extend(values)
                    if len(values) == 1:
                        self.__uncheckedsinglevalues__.append(tempmatrix[columnindex][rowindex])

    # Prunes a value (indicated by a reference to a cell) from all cells in the column indicated by columnindex.
    def pruneColumn(self, value, columnindex):
        tempcolumn = self.__tempsudoku__.getColumn(columnindex)
        for values in tempcolumn:
            if value[0] in values and value is not values:
                values.remove(value[0])
                self.valueCheck(value, values)

    # Prunes a value (indicated by a reference to a cell) from all cells in the row indicated by rowindex.
    def pruneRow(self, value, rowindex):
        temprow = self.__tempsudoku__.getRow(rowindex)
        for values in temprow:
            if value[0] in values and value is not values:
                self.valueCheck(value, values)
                values.remove(value[0])

    # Prunes a value (indicated by a reference to a cell) from all cells in the submatrix in which the cell indicated by the column and row indices is located.
    def pruneSubMatrix(self, value, columnindex, rowindex):
        tempsubmatrix = self.__tempsudoku__.getSubmatrixForPruning(columnindex, rowindex)
        for column in tempsubmatrix:
            for values in column:
                if value[0] in values and value is not values:
                    self.valueCheck(value, values)
                    values.remove(value[0])

    # Takes a reference to a cell as it's argument and runs all prune methods
    def pruneValue(self, valuetoprune):
        tempindex = self.__tempsudoku__.findIndex(valuetoprune)
        columnindex = tempindex[0]
        rowindex = tempindex[1]

        self.pruneSubMatrix(valuetoprune, columnindex, rowindex)
        self.pruneColumn(valuetoprune, columnindex)
        self.pruneRow(valuetoprune, rowindex)

    # Returns true if the sudoku is solved.
    def isSolved(self):
        if len(self.__checkedsinglevalues__) == self.__tempsudoku__.getSudokusize() ** 2:
            if self.areColumnsSolved() and self.areRowsSolved() and self.areSubmatricesSolved():
                return True
        else:
            return False

    # Returns true if all columns are solved.
    def areColumnsSolved(self):
        for columnindex, column in enumerate(self.__tempsudoku__.getMatrix()):
            possiblevalues = copy.deepcopy(self.getAllPossibleValues())
            for value in column:
                if value[0] not in possiblevalues:
                    self.__paradox__ = True
                    return False
                possiblevalues.remove(value[0])
            if len(possiblevalues):
                return False
        return True

    # Returns true if all rows are solved.
    def areRowsSolved(self):
        for rowindex, column in enumerate(self.__tempsudoku__.getMatrix()):
            possiblevalues = copy.deepcopy(self.getAllPossibleValues())
            for value in self.__tempsudoku__.getRow(rowindex):
                if value[0] not in possiblevalues:
                    self.__paradox__ = True
                    return False
                possiblevalues.remove(value[0])
            if len(possiblevalues):
                return False
        return True

    # Returns true if all submatrices are solved.
    def areSubmatricesSolved(self):
        submatrices = self.__tempsudoku__.getSubMatrices()
        for submatrix in submatrices:
            possiblevalues = copy.deepcopy(self.getAllPossibleValues())
            for column in submatrix:
                for value in column:
                    if value[0] not in possiblevalues:
                        self.__paradox__ = True
                        return False
                    possiblevalues.remove(value[0])
            if len(possiblevalues):
                return False
        return True

    # Returns a new matrix based on the two inputted sudokus; this matrix is used in the solve() method in co-junction with the isDiffMatrixEmpty method and the if-statement at the end of solve() in order to determine if the sudoku is as solved as this class can make it.
    def getDiffMatrix(self, oldsudoku, newsudoku):
        diffmatrix = []
        for columnindex, column in enumerate(oldsudoku.getMatrix()):
            diffmatrix.append([])
            for rowindex, row in enumerate(column):
                diffmatrix[columnindex].append([])
                for value in row:
                    if value not in newsudoku.getMatrix()[columnindex][rowindex]:
                        diffmatrix[columnindex][rowindex].append(value * -1)
        return diffmatrix

    # Returns true if the inputted matrix is empty.
    def isDiffMatrixEmpty(self, diffmatrix):
        for column in diffmatrix:
            for row in column:
                if len(row):
                    return False
        return True

    # Solves the sudoku.
    def solve(self):
        while not self.isSolved():
            oldsudoku = copy.deepcopy(self.__tempsudoku__)

            if len(self.__uncheckedsinglevalues__):
                uncheckedvalue = self.__uncheckedsinglevalues__.pop(0)
                self.pruneValue(uncheckedvalue)
                self.__checkedsinglevalues__.append(uncheckedvalue)

            if not len(self.__uncheckedsinglevalues__):
                for value in self.__tempsudoku__.getSingleValues():
                    temp = True
                    for values in self.__checkedsinglevalues__:
                        if value is values:
                            temp = False
                    for values in self.__uncheckedsinglevalues__:
                        if value is values:
                            temp = False
                    if temp:
                        self.__uncheckedsinglevalues__.append(value)

            # This if-statement checks to see if the sudoku is as solved as this class can make it; if it is, and still isn't entirely solved, it simply sets the matrix in the sudoku to an empty list before ending itself.
            if self.isDiffMatrixEmpty(self.getDiffMatrix(oldsudoku, self.__tempsudoku__)) and not (len(self.__uncheckedsinglevalues__) or len(self.__checkedsinglevalues__) == (self.__tempsudoku__.getSudokusize() ** 2)):
                self.__tempsudoku__.setMatrix([])
                break
