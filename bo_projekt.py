import numpy as np
from typing import List, Any

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

    # powiększanie fi o element minimalny

    return phi + minimum
    


def krok4_test():
    test_matrix = [[0, 0, 1, 0, 5],
                   [1, 6, 2, 0, 3],
                   [1, 2, 1, 5, 0],
                   [3, 9, 0, 4, 0],
                   [1, 1, 2, 4, 0]]
    
    h_lines = [0, 1, 3]
    v_lines = [4]
    phi = 6

    phi = krok4(v_lines, h_lines, test_matrix, phi)

    print(phi, "\n")

    for row in test_matrix:
        print(row)

krok4_test()