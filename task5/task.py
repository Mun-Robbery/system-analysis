import json
import numpy as np

def get_rankings(structure):
    rankings = {}
    for idx, item in enumerate(structure):
        elements = item if isinstance(item, list) else [item]
        for elem in elements:
            rankings[elem] = idx
    return rankings

def build_matrix(rankings):
    size = len(rankings)
    matrix = []
    for i in range(1, size + 1):
        row = [1 if rankings[key] >= rankings[i] else 0 for key in rankings]
        matrix.append(row)
    return matrix

def compute_kernel(mat_a, mat_b):
    arr_a = np.array(mat_a)
    arr_b = np.array(mat_b)
    return np.logical_or(arr_a * arr_b, arr_a.T * arr_b.T)

def main(data_a, data_b):
    rankings_a = get_rankings(data_a)
    rankings_b = get_rankings(data_b)
    matrix_a = build_matrix(rankings_a)
    matrix_b = build_matrix(rankings_b)
    kernel = compute_kernel(matrix_a, matrix_b)
    print(kernel)

if __name__ == "__main__":
    input_a = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
    input_b = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]
    main(input_a, input_b)
