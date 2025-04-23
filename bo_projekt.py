import numpy as np
import copy


#działa dla przykładu z wykładu i guess
def alg1(a, zeros):
    """
    Wyznacza minimalny zbiór linii wykreślających wszystkie zera w macierzy.
    - a: macierz kosztów
    - zeros: macierz oznaczeń zera w `a`:
            - 1 oznacza zero niezależne
            - -1 oznacza zero zależne
            - None oznacza brak znaczenia

    Zwraca:
    - crossrow: lista określająca, które wiersze należy przekreślić (True = przekreślony)
    - crosscol: lista określająca, które kolumny należy przekreślić (True = przekreślona)
    """

    #Inicjalizacja danych
    h, w = a.shape
    rows = [False for i in range(h)] #True jak zaznaczony wiersz
    cols = [False for i in range(w)] #True jak zaznaczona kolumna

    #Poszukiwanie maksymalnego skojarzenia
    while True:
        rowpre = copy.deepcopy(rows)
        colpre = copy.deepcopy(cols)
        #Oznaczanie każdego wiersza nie posiadającego niezależnego zera 
        for i in range(h):
            if 1 not in zeros[i]:
                rows[i] = True
        #Oznaczyanie każdej kolumny mającej zero zależne w oznaczonym wierszu
        for i in range(w):
            for j in range(h):
                if rows[j] and zeros[j, i] == -1:
                    cols[j] = True
        #Oznaczanie każdego wiersza mającego w oznakowanej kolumnie niezależne zero 
        for i in range(h):
            for j in range(w):
                if cols[j] and zeros[i, j] == 1:
                    rows[i] = True
        #Pętle należy kontynuować tak długo, aż nie jest możliwe dalsze oznakowanie     
        if rows == rowpre and cols == colpre:
            break

    #Poszukiwanie minimalnego pokrycia wierzchołkowego
    crossrow = [False for i in range(h)]
    crosscol = [False for i in range(w)]
    #Przekreślamy wszystkie nieoznakowane wiersze oraz oznakowane kolumny
    for i in range(h):
        if not rows[i]:
            crossrow[i] = True
    for i in range(w):
        if cols[i]:
            crosscol[i] = True

    return crossrow, crosscol

