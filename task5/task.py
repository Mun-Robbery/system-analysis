import json
import typing as tp

RANGING_A = "[1, [2, 3], 4, [5, 6, 7], 8, 9, 10]"
RANGING_B = "[[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]"

Matrix = list[list[int]]
Range = list[tp.Union[list[int], int]]

def create_matrix_from_range(input_range: Range) -> Matrix:
    value_to_index = {}
    for index, item in enumerate(input_range):
        if isinstance(item, list):
            for sub_item in item:
                value_to_index[sub_item] = index
        else:
            value_to_index[item] = index

    size = len(value_to_index)
    matrix = [[0] * size for _ in range(size)]

    for key1, idx1 in sorted(value_to_index.items()):
        for key2, idx2 in sorted(value_to_index.items()):
            if idx2 <= idx1:
                matrix[key1 - 1][key2 - 1] = 1
    return matrix

def logical_and_matrices(matrix1: Matrix, matrix2: Matrix) -> Matrix:
    rows = len(matrix1)
    cols = len(matrix1[0])
    return [[matrix1[i][j] & matrix2[i][j] for j in range(cols)] for i in range(rows)]

def main(range_str1: str, range_str2: str) -> str:
    range1 = json.loads(range_str1)
    range2 = json.loads(range_str2)
    
    matrix1 = create_matrix_from_range(range1)
    matrix2 = create_matrix_from_range(range2)
    
    combined_matrix = logical_and_matrices(matrix1, matrix2)
    result_pairs = []

    for row_idx in range(len(combined_matrix)):
        for col_idx in range(row_idx + 1, len(combined_matrix[row_idx])):
            if combined_matrix[row_idx][col_idx] == combined_matrix[col_idx][row_idx]:
                result_pairs.append([row_idx + 1, col_idx + 1])

    return json.dumps(result_pairs)

if __name__ == "__main__":
    output = main(RANGING_A, RANGING_B)
    print(output)
