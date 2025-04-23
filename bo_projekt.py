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
    


    