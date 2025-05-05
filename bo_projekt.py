import numpy as np
import copy

#redukcja macierzy
def reduction(A):
    phi = 0
    A1 = []

    for row in A:
        min1 = min(row)
        phi += min1
        new_row = row - min1
        A1.append(new_row)
    
    A1 = np.array(A1)
    A1 = A1.T
    A2 = []
    
    for col in A1:
        min2 = min(col)
        phi += min2
        new_col = col - min(col)
        A2.append(new_col)

    A2 = np.array(A2)
    return A2.T, phi

# do usunięcia, ale działa jak na wykładzie
A1 = np.array([[5, 2, 3, 2, 7],
               [6, 8, 4, 2, 5],
               [6, 4, 3, 7, 2],
               [6, 9, 0, 4, 0],
               [4, 1, 2, 4, 0]])

result = reduction(A1)
print('Zredukowana macierz:\n{0}\n\nphi: {1}'.format(result[0], result[1]))
from typing import List, Any



def krok4(vertical_lines : List[int], horizontal_lines : List[int], matrix : List[List[Any]], fi : List[Any]):
    """
    krok 4 algorytmu wegierskiego.

    Args:
        vertical_lines (List[int]): Lista indeksów kolumn przykrytych liniami pionowymi.
        horizontal_lines (List[int]): Lista indeksów wierszy przykrytych liniami poziomymi.
        matrix (List[List[Any]]): Macierz, na której wykonywane są operacje.
        fi (List[Any]): argument fi przekazywany jako jednoelementowa tablica [fi]

    Returns:
        None: Funkcja modyfikuje macierz w miejscu.
    """
        
    inf = float("inf")
    minimum = inf

    for y, row in enumerate(matrix):    # znajdowanie minimalnego elementu nieprzykrytego liniami
        for x, el in row:
            if x not in vertical_lines:
                if y not in horizontal_lines:
                    if el < minimum:
                        minimum = el

    for y, row in enumerate(matrix):    # odejmowanie znalezionego elementu od wszystkich elementów nieprzykrytych liniami
        for x, el in row:
            if x not in vertical_lines:
                if y not in horizontal_lines:
                    matrix[y][x] -= minimum


    for y, row in enumerate(matrix):    # odejmowanie znalezionego elementu od wszystkich elementów nieprzykrytych liniami
        for x, el in row:
            if x in vertical_lines:
                if y in horizontal_lines:
                    matrix[y][x] += minimum

    # powiększanie fi
    




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

