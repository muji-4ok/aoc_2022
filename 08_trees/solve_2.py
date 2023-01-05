from pprint import pprint
import itertools

def column_list(matrix: list[list[int]], i: int) -> list[int]:
    return [matrix[j][i] for j in range(len(matrix))]


def count_visible(i: int, l: list[int]) -> (int, int):
    left_visible = 0

    for j in range(i - 1, -1, -1):
        left_visible += 1

        if l[j] >= l[i]:
            break

    right_visible = 0

    for j in range(i + 1, len(l)):
        right_visible += 1

        if l[j] >= l[i]:
            break

    return left_visible, right_visible


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

heights = [[int(c) for c in line] for line in lines]
best_score = 0

for i in range(len(heights)):
    for j in range(len(heights[0])):
        left, right = count_visible(j, heights[i])
        up, down = count_visible(i, column_list(heights, j))
        score = left * right * up * down
        best_score = max(best_score, score)

print(best_score)

