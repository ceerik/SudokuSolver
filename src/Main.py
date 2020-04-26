from src.sudoku import Sudoku
from src.SudokuSolver import SudokuSolver

# Example program to demonstrate the functionality of the sudoku solving class SudokuSolver, and its accompanying sudoku class.

# Example sudoku 1; Can't be solved by SudokuSolver:
matrix1 =   [
            [[8],   [],     [5],    [1],    [],     [],     [9],    [],     []],
            [[],    [],     [],     [6],    [],     [],     [],     [2],    []],
            [[],    [],     [9],    [],     [],     [],     [],     [6],    []],
            [[],    [],     [],     [],     [],     [],     [6],    [4],    []],
            [[1],   [],     [3],    [],     [],     [],     [],     [],     [5]],
            [[],    [],     [],     [5],    [2],    [],     [],     [1],    [8]],
            [[],    [],     [],     [],     [],     [4],    [],     [5],    []],
            [[],    [],     [6],    [],     [],     [],     [],     [],     []],
            [[],    [2],    [],     [],     [],     [1],    [3],    [],     []]
            ]

# Example sudoku 2; Can't be solved by SudokuSolver:
matrix2 =   [
            [[],    [9],    [],     [7],    [],     [4],    [],     [],     []],
            [[],    [],     [8],    [],     [2],    [],     [7],    [],     []],
            [[],    [],     [2],    [],     [6],    [],     [],     [],     [9]],
            [[1],   [],     [],     [],     [],     [],     [],     [],     []],
            [[],    [],     [],     [],     [],     [],     [],     [7],    [6]],
            [[2],   [],     [3],    [],     [7],    [],     [1],    [],     []],
            [[],    [],     [],     [],     [8],    [],     [4],    [],     [7]],
            [[3],   [2],    [7],    [],     [],     [],     [],     [9],    []],
            [[],    [4],    [],     [1],    [],     [],     [6],    [],     []]
            ]

# Example sudoku 3; Can be solved by SudokuSolver:
matrix3 =   [
            [[],    [9],    [],     [],     [2],    [],     [],     [],     [4]],
            [[6],   [1],    [],     [4],    [],     [9],    [],     [3],    []],
            [[4],   [],     [],     [],     [5],    [],     [9],    [7],    []],
            [[],    [],     [1],    [],     [6],    [4],    [],     [],     [9]],
            [[],    [2],    [],     [],     [],     [5],    [1],    [],     []],
            [[],    [6],    [8],    [],     [7],    [3],    [],     [2],    []],
            [[],    [],     [9],    [7],    [],     [6],    [2],    [5],    []],
            [[1],   [],     [],     [5],    [],     [2],    [],     [],     []],
            [[],    [3],    [5],    [],     [],     [],     [],     [],     [7]]
            ]

sudoku = Sudoku.makeSudoku(matrix3)

print(sudoku.getMatrix())

solvesudoku = sudoku.makeSudoku(SudokuSolver.actuallySolve(sudoku).getMatrix())

print("solved sudoku:", solvesudoku.getMatrix())
