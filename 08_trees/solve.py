from pprint import pprint

def column_list(matrix: list[list[int]], i: int) -> list[int]:
    return [matrix[j][i] for j in range(len(matrix))]


def is_visible(i: int, l: list[int]) -> bool:
    return i == 0 or i == len(l) - 1 or l[i] > min(max(l[:i]), max(l[i + 1:]))


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

heights = [[int(c) for c in line] for line in lines]

visible_count = 0

for i in range(len(heights)):
    for j in range(len(heights[0])):
        visible_count += is_visible(j, heights[i]) or is_visible(i, column_list(heights, j))

print(visible_count)
