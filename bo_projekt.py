import numpy as np

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