import random
import numpy as np
import math 
from random import choice
import statistics 

sudoku_iniziale = """
                    024007000
                    600000000
                    003680415
                    431005000
                    500000032
                    790000060
                    209710800
                    040093000
                    310004750
                """

sudoku = np.array([[int(i) for i in riga] for riga in sudoku_iniziale.split()])

def stampa_sudoku(sudoku):
    print("\n")
    for i in range(len(sudoku)):
        riga = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                riga += "| "
            riga += str(sudoku[i,j])+" "
        print(riga)

def fissa_valori_sudoku(sudoku_fisso):
    for i in range (0,9):
        for j in range (0,9):
            if sudoku_fisso[i,j] != 0:
                sudoku_fisso[i,j] = 1
    
    return(sudoku_fisso)