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

# Funzione Costo    
def calcola_numero_errori(sudoku):
    numero_errori = 0 
    for i in range (0,9):
        numero_errori += calcola_errori_riga_colonna(i ,i ,sudoku)
    return(numero_errori)

def calcola_errori_riga_colonna(riga, colonna, sudoku):
    numero_errori = (9 - len(np.unique(sudoku[:,colonna]))) + (9 - len(np.unique(sudoku[riga,:])))
    return(numero_errori)


def crea_blocchi_3x3():
    lista_blocchi_finali = []
    for r in range (0,9):
        lista_tmp = []
        blocco1 = [i + 3*((r)%3) for i in range(0,3)]
        blocco2 = [i + 3*math.trunc((r)/3) for i in range(0,3)]
        for x in blocco1:
            for y in blocco2:
                lista_tmp.append([x,y])
        lista_blocchi_finali.append(lista_tmp)
    return(lista_blocchi_finali)

def riempi_blocchi_3x3_casualmente(sudoku, lista_blocchi):
    for blocco in lista_blocchi:
        for casella in blocco:
            if sudoku[casella[0],casella[1]] == 0:
                blocco_corrente = sudoku[blocco[0][0]:(blocco[-1][0]+1),blocco[0][1]:(blocco[-1][1]+1)]
                sudoku[casella[0],casella[1]] = choice([i for i in range(1,10) if i not in blocco_corrente])
    return sudoku
