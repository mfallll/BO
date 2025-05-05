import numpy as np
import copy
from typing import List, Any, Tuple

def reduction(A: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Wykonuje redukcję wierszy i kolumn oraz znajduje dolne ograniczenie wartości funkcji celu phi.
    - A (np.ndarray): macierz, na której wykonywane są operacje.

    Zwraca:
    - A2 (np.ndarray): zredukowana macierz kosztów
    - phi (float): dolne ograniczenie funkcji celu
    """

    #Inicjalizacja zmiennych
    phi = 0
    A1 = []

    for row in A: #Dla każdego rzędu macierzy A
        min1 = min(row) #Znajduje minimalny element w danym rzędzie
        phi += min1
        new_row = row - min1
        A1.append(new_row) #Kolejny rząd nowej macierzy - odpowiadający mu rząd macierzy A
        #pomniejszony o jego minimalny element
    
    #Inicjalizacja zmiennych
    A1 = np.array(A1)
    A1 = A1.T
    A2 = []
    
    for col in A1: #Dla każdej kolumny macierzy A1
        min2 = min(col) #Znajduje minimalny element w danej kolumnie
        phi += min2
        new_col = col - min(col)
        A2.append(new_col) #Kolejna kolumna nowej macierzy - odpowiadająca jej kolumna macierzy A1
        #pomniejszona o jej minimalny element

    A2 = np.array(A2)
    A2 = A2.T
    return A2, phi

def krok4(vertical_lines: List[int], horizontal_lines: List[int], matrix: List[List[Any]], phi: float) -> float:
    """
    Realizuje krok 4 algorytmu wegierskiego -modyfikację macierzy na podstawie minimalnego nieprzykrytego elementu.
    - vertical_lines (List[int]): indeksy kolumn przykrytych liniami pionowymi.
    - horizontal_lines (List[int]): lista indeksy wierszy przykrytych liniami poziomymi.
    - matrix (List[List[Any]]): macierz kosztów do modyfikacji.
    - phi (float): bieżąca wartość funkcji celu

    Zwraca:
    - phi (float): zmodyfikowana wartość funkcji celu.
    """
        
    inf = float("inf")
    minimum = inf

    for y, row in enumerate(matrix):    #Znajdowanie minimalnego elementu nieprzykrytego liniami
        for x, el in enumerate(row):
            if x not in vertical_lines:
                if y not in horizontal_lines:
                    if el < minimum:
                        minimum = el

    for y, row in enumerate(matrix):    #Odejmowanie znalezionego elementu od wszystkich elementów nieprzykrytych liniami
        for x, el in enumerate(row):
            if x not in vertical_lines:
                if y not in horizontal_lines:
                    matrix[y][x] -= minimum


    for y, row in enumerate(matrix):    #Dodawanie minimum do wszystkich elementów na przecięciach
        for x, el in enumerate(row):
            if x in vertical_lines:
                if y in horizontal_lines:
                    matrix[y][x] += minimum

    #Powiększanie fi o element minimalny
    return phi + minimum

def alg1(a: np.ndarray, zeros: np.ndarray) -> Tuple[List[int], List[int]]:
    """
    Wyznacza minimalny zbiór linii wykreślających wszystkie zera w macierzy.
    - a (np.ndarray): macierz kosztów
    - zeros(np.ndarray): macierz oznaczeń zera, gdzie:
            - -1 oznacza zero niezależne
            - -2 oznacza zero zależne

    Zwraca:
    - crossrow (List[int]): lista określająca, które wiersze należy przekreślić
    - crosscol (List[int]): lista określająca, które kolumny należy przekreślić
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
        #Oznaczanie każdej kolumny mającej zero zależne w oznaczonym wierszu
        for i in range(w):
            for j in range(h):
                if rows[j] and zeros[j, i] == -2:
                    cols[i] = True
        #Oznaczanie każdego wiersza mającego w oznakowanej kolumnie niezależne zero 
        for i in range(h):
            for j in range(w):
                if cols[j] and zeros[i, j] == -1:
                    rows[i] = True
        #Pętle należy kontynuować tak długo, aż nie jest możliwe dalsze oznakowanie     
        if rows == rowpre and cols == colpre:
            break

    #Poszukiwanie minimalnego pokrycia wierzchołkowego
    crossrow = []
    crosscol = []
    #Przekreślamy wszystkie nieoznakowane wiersze oraz oznakowane kolumny
    for i in range(h):
        if not rows[i]:
            crossrow.append(i)
    for i in range(w):
        if cols[i]:
            crosscol.append(i)

    return crossrow, crosscol
    
def zera_niezal_zachl(A: np.ndarray) -> Tuple[np.ndarray, str]:
    """
    Znajduje zbiór niezależnych zer w macierzy kosztów przy użyciu zachłannego algorytmu.
    - A (np.ndarray): macierz kosztów (zawierająca zera, które mają zostać pokryte).
    
    Zwraca:
    - A_work (np.ndarray): macierz oznaczeń zera, gdzie:
        - -1 oznacza zero niezależne,
        - -2 oznacza zero zależne,
    - status (str): 
        - "DONE" jeśli wszystkie kolumny zostały pokryte zerami niezależnymi,
        - "NOT_DONE" jeśli nie udało się pokryć wszystkich kolumn.
    """

    #Inicjalizacja zmiennych
    A_work = copy.deepcopy(A)
    size = A.shape[0]
    rem_col = set([x for x in range(size)])
    rem_row = set([x for x in range(size)])

    while True:
        stop = True
        B = np.zeros((size, size)) + np.inf
        for y in rem_col:
            for x in rem_row:
                if A[x, y] == 0:
                    #Liczba zer w tym wierszu i kolumnie
                    B[x, y] = len([1 for i in rem_col if A[x, i] == 0]) + len([1 for i in rem_row if A[i, y] == 0]) - 2
                    stop = False

        #Gdy nie ma już więcej zer do rozważenia
        if stop:
            A_work[A_work == 0] = -2
            if len(rem_col) == 0:
                return A_work, 'DONE'
            else:
                return A_work, 'NOT_DONE'
            
        else:
            #Wybiera zero zabierające najmniej innych zer
            x_min, y_min = np.unravel_index(np.argmin(B, axis=None), B.shape)
            A_work[x_min, y_min] = -1 #Oznacza jako niezależne
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

def schemat_ogl(matrix: np.ndarray) -> None:
    """
    Wykonuje schemat ogólny algorytmu węgierskiego w celu rozwiązania problemu przyporządkowania.
    - matrix (np.ndarray): macierz kosztów, dla której szukane jest optymalne przyporządkowanie.
    """
    print(f"Macierz początkowa: \n {matrix}")

    #Krok 1: Redukcja macierzy (krok przygotowywawczy)
    matrix, phi = reduction(matrix)
    print(f"Macierz po redukcji: \n {matrix}")
    print(f"Dolne ograniczenie funkcji celu: {phi}")

    while True:
        #Krok 2: Znalezienie zbioru niezależnych zer
        macierz_zer, info = zera_niezal_zachl(matrix)

        if info == 'DONE':
            #Jeśli znaleziono kompletny przydział – wypisz rozwiązanie
            print('Rozwiązanie x:')
            macierz_zer[macierz_zer != -1] = 0
            macierz_zer[macierz_zer == -1] = 1
            print(macierz_zer)
            print(f"Sumaryczny koszt: {phi}")
            return

         #Krok 4: Wyznaczenie minimalnego zbioru linii wykreślających wszystkie zera
        [hori_lines, vert_lines] = alg1(matrix, macierz_zer)
        print(f"Rzędy do wykreślenia: {hori_lines}")
        print(f"Kolumny do wykreślenia: {vert_lines}")
         #Krok 5: Próba powiększenia zbioru zer niezależnych
        phi = krok4(vert_lines, hori_lines, matrix, phi)
        print(f"Macierz z powiększonych zbiorem zer niezależnych: \n{matrix}")
        print(f"Nowe ograniczenie dolne {phi}")



matrix = np.array([
    [58, 80, 20, 64, 9, 95],
    [5, 3, 21, 14, 32, 47],
    [18, 82, 53, 79, 24, 31],
    [23, 30, 42, 49, 63, 63],
    [20, 51, 25, 77, 84, 26],
    [18, 45, 99, 14, 17, 9]
])
    
schemat_ogl(matrix)

