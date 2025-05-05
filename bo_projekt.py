import numpy as np
import copy
from typing import List, Any

# redukcja macierzy
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

def krok4(vertical_lines : List[int], horizontal_lines : List[int], matrix : List[List[Any]], phi : Any):
    """
    krok 4 algorytmu wegierskiego.

    Args:
        vertical_lines (List[int]): Lista indeksów kolumn przykrytych liniami pionowymi.
        horizontal_lines (List[int]): Lista indeksów wierszy przykrytych liniami poziomymi.
        matrix (List[List[Any]]): Macierz, na której wykonywane są operacje.
        phi (List[Any]): argument phi

    Returns:
        phi: zmodyfikowane fi
    """
        
    inf = float("inf")
    minimum = inf

    for y, row in enumerate(matrix):    # znajdowanie minimalnego elementu nieprzykrytego liniami
        for x, el in enumerate(row):
            if x not in vertical_lines:
                if y not in horizontal_lines:
                    if el < minimum:
                        minimum = el

    for y, row in enumerate(matrix):    # odejmowanie znalezionego elementu od wszystkich elementów nieprzykrytych liniami
        for x, el in enumerate(row):
            if x not in vertical_lines:
                if y not in horizontal_lines:
                    matrix[y][x] -= minimum


    for y, row in enumerate(matrix):    # odejmowanie znalezionego elementu od wszystkich elementów nieprzykrytych liniami
        for x, el in enumerate(row):
            if x in vertical_lines:
                if y in horizontal_lines:
                    matrix[y][x] += minimum

    # powiększanie fi
    # powiększanie fi o element minimalny
    return phi + minimum

def alg1(a, zeros):
    """
    Wyznacza minimalny zbiór linii wykreślających wszystkie zera w macierzy.
    - a: macierz kosztów
    - zeros: macierz oznaczeń zera w `a`:
            - -1 oznacza zero niezależne
            - -2 oznacza zero zależne

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
            if -1 not in zeros[i]:
                rows[i] = True
        #Oznaczyanie każdej kolumny mającej zero zależne w oznaczonym wierszu
        for i in range(w):
            for j in range(h):
                if rows[j] and zeros[j, i] == -2:
                    cols[j] = True
        #Oznaczanie każdego wiersza mającego w oznakowanej kolumnie niezależne zero 
        for i in range(h):
            for j in range(w):
                if cols[j] and zeros[i, j] == -1:
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
    
def zera_niezal_zachl(A: np.ndarray):
    # zero zabierające najmniej zer
    size = A.shape[0]
    rem_col = set([x for x in range(size)])
    rem_row = set([x for x in range(size)])
    while True:
        stop = True
        B = np.zeros((size, size)) + np.inf
        for y in rem_col:
            for x in rem_row:
                if A[x, y] == 0:
                    B[x, y] = len([1 for i in rem_col if A[x, i] == 0]) + len([1 for i in rem_row if A[i, y] == 0]) - 2
                    stop = False
        # zabieramy najmniejszy element albo kończymy
        if stop:
            A[A == 0] = -2
            if len(rem_col) == 0:
                return A, 'DONE'
            else:
                return A, 'NOT_DONE'
        else:
            x_min, y_min = np.unravel_index(np.argmin(B, axis=None), B.shape)
            A[x_min, y_min] = -1
            rem_col.remove(y_min)
            rem_row.remove(x_min)

'''
# alg. Munkresa
class Super_break(Exception):
    pass

def zera_niezal(A: np.ndarray):

    """
    zera niezależne
    0 - zero nieoznaczone
    -1 - zero niezależne
    -2 - zero zależne

    return:
    A - macierz z oznaczonymi zerami
    marked_col/marked_row - oznaczone kolumny/wiersze
    DONE/NOT_DONE - informacja czy program znalazł ostateczne rozwiązanie
    """


    def stop_loop(A, row, col):
        size = A.shape[0]
        done = True
        for j in range(size):
            for i in range(size):
                if A[i, j] in [0, -1, -2] and i not in row and j not in col:
                    done = False
                    break
            else:
                continue
            break
        return done

    size = A.shape[0]
    # oznaczanie 0*
    for y in range(size):
        for x in range(size):
            if A[x, y] == 0 and -1 not in A[x, :] and -1 not in A[:, y]:
                A[x, y] = -1
    while True:
        # pokrycie 0*
        marked_col = set([])
        marked_row = set([])
        for y in range(size):
            if -1 in A[:, y]:
                marked_col.add(y)
        # znalezione rozwiązanie optymalne/nieoptymalne
        if len(marked_col) == size:
            return A, list(marked_col), list(marked_row), 'DONE'
        elif stop_loop(A, marked_row, marked_col):
            return A, list(marked_col), list(marked_row), 'DONE'
        # oznaczenie zer prim
        try:
            for x in range(size):
                for y in range(size):
                    if A[x, y] == 0 and y not in marked_col and x not in marked_row:
                        A[x, y] = -2
                        if -1 not in A[x, :]:
                            # konstrukcja serii
                            star_coord = []
                            prim_coord = []
                            prim_coord.append((x, y))
                            while -1 in A[:, y]:
                                x = int(np.nonzero(A[:, y] == -1)[0][0])
                                star_coord.append((x, y))
                                y = int(np.nonzero(A[x, :] == -2)[0][0])
                                prim_coord.append((x, y))
                            # zmiana oznaczeń
                            for x, y in star_coord:
                                A[x, y] = 0
                            for x, y in prim_coord:
                                A[x, y] = -1
                            # usunięcie primów
                            A[A == -2] = 0
                            raise Super_break()
                        else:
                            y_r = int(np.nonzero(A[x, :] == -1)[0][0])
                            marked_row.add(x)
                            marked_col.remove(y_r)
                            # warunek stopu
                            if stop_loop(A, marked_row, marked_col):
                                return A, list(marked_col), list(marked_row), 'DONE'
        except Super_break:
            pass
'''

def main():
    macierz_z_wykladu = np.array([[5, 2, 3, 2, 7],
                                  [6, 8, 4, 2, 5],
                                  [6, 4, 3, 7, 2],
                                  [6, 9, 0, 4, 0],
                                  [4, 1, 2, 4, 0]])
    macierz_z_wykladu, phi = reduction(macierz_z_wykladu)
    while True:
        print(macierz_z_wykladu, phi)
        macierz_zer, info = zera_niezal_zachl(macierz_z_wykladu)
        if info == 'DONE':
            print('Rozwiązanie x:')
            print(macierz_z_wykladu[macierz_zer == -1].astype('uint8'))
            print(f"Sumaryczny koszt: {phi}")
            return
        print(macierz_zer)

        # wykreślanie zer
        [hori_lines, vert_lines] = alg1(macierz_z_wykladu, macierz_zer)
        print(vert_lines)
        print(hori_lines)
        phi = krok4(vert_lines, hori_lines, macierz_z_wykladu, phi)
        print(macierz_z_wykladu)
        return
main()
