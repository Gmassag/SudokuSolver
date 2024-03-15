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

def somma_di_un_blocco(sudoku, un_blocco):
    somma_finale = 0
    for casella in un_blocco:
        somma_finale += sudoku[casella[0], casella[1]]
    return(somma_finale)

def due_caselle_casuali_nel_blocco(sudoku_fisso, blocco):
    while (1):
        prima_casella = random.choice(blocco)
        seconda_casella = choice([casella for casella in blocco if casella is not prima_casella ])

        if sudoku_fisso[prima_casella[0], prima_casella[1]] != 1 and sudoku_fisso[seconda_casella[0], seconda_casella[1]] != 1:
            return([prima_casella, seconda_casella])

def scambia_caselle(sudoku, caselle_da_scambiare):
    sudoku_proposto = np.copy(sudoku)
    segnaposto = sudoku_proposto[caselle_da_scambiare[0][0], caselle_da_scambiare[0][1]]
    sudoku_proposto[caselle_da_scambiare[0][0], caselle_da_scambiare[0][1]] = sudoku_proposto[caselle_da_scambiare[1][0], caselle_da_scambiare[1][1]]
    sudoku_proposto[caselle_da_scambiare[1][0], caselle_da_scambiare[1][1]] = segnaposto
    return (sudoku_proposto)

def stato_proposto(sudoku, sudoku_fisso, lista_blocchi):
    blocco_casuale = random.choice(lista_blocchi)

    if somma_di_un_blocco(sudoku_fisso, blocco_casuale) > 6:  
        return(sudoku, 1, 1)
    caselle_da_scambiare = due_caselle_casuali_nel_blocco(sudoku_fisso, blocco_casuale)
    sudoku_proposto = scambia_caselle(sudoku,  caselle_da_scambiare)
    return([sudoku_proposto, caselle_da_scambiare])

def scegli_nuovo_stato(sudoku_corrente, sudoku_fisso, lista_blocchi, sigma):
    proposta = stato_proposto(sudoku_corrente, sudoku_fisso, lista_blocchi)
    nuovo_sudoku = proposta[0]
    caselle_da_controllare = proposta[1]
    costo_corrente = calcola_errori_riga_colonna(caselle_da_controllare[0][0], caselle_da_controllare[0][1], sudoku_corrente) + calcola_errori_riga_colonna(caselle_da_controllare[1][0], caselle_da_controllare[1][1], sudoku_corrente)
    nuovo_costo = calcola_errori_riga_colonna(caselle_da_controllare[0][0], caselle_da_controllare[0][1], nuovo_sudoku) + calcola_errori_riga_colonna(caselle_da_controllare[1][0], caselle_da_controllare[1][1], nuovo_sudoku)
    costo_differenza = nuovo_costo - costo_corrente
    rho = math.exp(-costo_differenza/sigma)
    if(np.random.uniform(1,0,1) < rho):
        return([nuovo_sudoku, costo_differenza])
    return([sudoku_corrente, 0])


def scegli_numero_iterazioni(sudoku_fisso):
    numero_iterazioni = 0
    for i in range (0,9):
        for j in range (0,9):
            if sudoku_fisso[i,j] != 0:
                numero_iterazioni += 1
    return numero_iterazioni

def calcola_sigma_iniziale(sudoku, sudoku_fisso, lista_blocchi):
    lista_differenze = []
    tmp_sudoku = sudoku
    for i in range(1,10):
        tmp_sudoku = stato_proposto(tmp_sudoku, sudoku_fisso, lista_blocchi)[0]
        lista_differenze.append(calcola_numero_errori(tmp_sudoku))
    return (statistics.pstdev(lista_differenze))
