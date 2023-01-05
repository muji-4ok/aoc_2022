from collections import deque


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

heights = []
start_x = 0
start_y = 0
end_x = 0
end_y = 0

for y, line in enumerate(lines):
    heights.append([])

    for x, c in enumerate(line):
        if c == 'S':
            start_x = x
            start_y = y
            c = 'a'

        if c == 'E':
            end_x = x
            end_y = y
            c = 'z'

        heights[-1].append(ord(c) - ord('a'))

h = len(heights)
w = len(heights[0])

q = deque([(start_x, start_y)])
distance_to = {(start_x, start_y): 0}

while len(q):
    point = q.popleft()
    x, y = point

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_x = x + dx
        new_y = y + dy

        if not (0 <= new_x < w and 0 <= new_y < h):
            continue

        new_point = new_x, new_y

        if new_point in distance_to:
            continue

        if heights[new_y][new_x] - heights[y][x] > 1:
            continue

        distance_to[new_point] = distance_to[point] + 1
        q.append(new_point)

print(distance_to[(end_x, end_y)])
