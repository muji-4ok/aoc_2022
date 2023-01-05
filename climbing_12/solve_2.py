from collections import deque


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

heights = []
end_x = 0
end_y = 0
starts = []

for y, line in enumerate(lines):
    heights.append([])

    for x, c in enumerate(line):
        if c == 'S':
            c = 'a'

        if c == 'E':
            end_x = x
            end_y = y
            c = 'z'

        if c == 'a':
            starts.append((x, y))

        heights[-1].append(ord(c) - ord('a'))

end = end_x, end_y
h = len(heights)
w = len(heights[0])

best_distance = 100000

for start in starts:
    q = deque([start])
    distance_to = {start: 0}

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

            if new_point == end:
                q.clear()
                break

            q.append(new_point)

    if end in distance_to and distance_to[end] < best_distance:
        best_distance = distance_to[end]

print(best_distance)
