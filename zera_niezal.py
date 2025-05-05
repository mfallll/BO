import numpy as np
from typing import List, Any

# szukanie zer niezależnych
class Super_break(Exception):
    pass

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
            if len(rem_col) == 0:
                return A, 'DONE'
            else:
                return A, 'NOT_DONE'
        else:
            x_min, y_min = np.unravel_index(np.argmin(B, axis=None), B.shape)
            A[x_min, y_min] = -1
            rem_col.remove(y_min)
            rem_row.remove(x_min)

# BŁAGAM NIE URUCHAMIAJCIE DLA DUŻYCH MACIERZY
# TEN POTWÓR MA ZŁOŻONOŚĆ n!**2

def zera_niezal_full(A: np.ndarray):

    def zera_rek(A: np.ndarray, rows, cols, coord, lists):
        if A.shape[0] == 1:
            if A[0,0] == 0:
                coord.append((rows[0], cols[0]))
            lists.append(coord)
            return lists
        deeper = False
        for y in range(A.shape[0]):
            for x in range(A.shape[0]):
                if A[x, y] == 0:
                    deeper = True
                    lists = zera_rek(np.delete(np.delete(A, y, 1), x, 0), rows[:y]+rows[y+1:], cols[:x]+cols[x+1:], coord + [(rows[y], cols[x])], lists)
        if not deeper:
            lists.append(coord)
        return lists

    lists = zera_rek(A, [x for x in range(A.shape[0])], [x for x in range(A.shape[0])], [], [])
    # lista z najwiekszą ilościa zer:
    z_max = 0
    coord_max = None
    for elem in lists:
        if len(elem) > z_max:
            z_max = len(elem)
            coord_max = elem
    # zaznaczanie zer
    for x, y in coord_max:
        A[x, y] = -1
    if len(coord_max) == A.shape[0]:
        return A, 'DONE'
    else:
        return A, 'NOT_DONE'

def zera_niezal(A: np.ndarray):

    '''
    zera niezależne
    0 - zero nieoznaczone
    -1 - zero niezależne
    -2 - zero zależne

    return:
    A - macierz z oznaczonymi zerami
    marked_col/marked_row - oznaczone kolumny/wiersze
    DONE/NOT_DONE - informacja czy program znalazł ostateczne rozwiązanie
    '''

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
            return A, list(marked_col), list(marked_row), 'NOT_DONE'
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
                                return A, list(marked_col), list(marked_row), 'NOT_DONE'
        except Super_break:
            pass

A = np.array([[0, 0, 0],
              [0, 1, 1],
              [0, 1, 1]])
print(zera_niezal(A))
print()
A = np.array([[0, 0, 0],
              [0, 1, 1],
              [0, 1, 1]])
print(zera_niezal_zachl(A))
print()
A = np.array([[0, 0, 0],
              [0, 1, 1],
              [0, 1, 1]])
print(zera_niezal_full(A))
