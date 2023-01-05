def add_line(start: tuple[int, int], end: tuple[int, int], field: set[tuple[int, int]]):
    if start[0] == end[0]:
        x = start[0]
        y_min = min(start[1], end[1])
        y_max = max(start[1], end[1])

        for y in range(y_min, y_max + 1):
            field.add((x, y))
    elif start[1] == end[1]:
        y = start[1]
        x_min = min(start[0], end[0])
        x_max = max(start[0], end[0])

        for x in range(x_min, x_max + 1):
            field.add((x, y))
    else:
        assert False


def move_sand(x: int, y: int, field: set[tuple[int, int]]) -> (int, int):
    if (x, y + 1) not in field:
        return x, y + 1
    elif (x - 1, y + 1) not in field:
        return x - 1, y + 1
    elif (x + 1, y + 1) not in field:
        return x + 1, y + 1
    else:
        return x, y


with open('sample_input.txt') as f:
    lines = f.read().split('\n')[:-2]

sand_start = 500, 0
field = set()

for line in lines:
    points = line.split(' -> ')
    points = list(map(lambda p: tuple(map(int, p.split(','))), points))

    for p1, p2 in zip(points, points[1:]):
        add_line(p1, p2, field)

max_y = max(p[1] for p in field)
min_x = min(p[0] for p in field)
max_x = max(p[0] for p in field)
sand_fallen = 0

add_line((min_x - max_y, max_y + 2), (max_x + max_y, max_y + 2), field)

while True:
    if sand_start in field:
        break

    x, y = sand_start

    while True:
        new_x, new_y = move_sand(x, y, field)

        if new_x == x and new_y == y:
            break

        x = new_x
        y = new_y

    field.add((x, y))
    sand_fallen += 1

print(sand_fallen)

