import sys


def free_sides(x: int, y: int, z: int) -> int:
    result = 0

    for dx in [-1, 1]:
        if (x + dx, y, z) in external_air:
            result += 1

    for dy in [-1, 1]:
        if (x, y + dy, z) in external_air:
            result += 1

    for dz in [-1, 1]:
        if (x, y, z + dz) in external_air:
            result += 1

    return result


def find_external_air(x: int, y: int, z: int):
    if (x, y, z) in external_air:
        return

    if not ((min_x - 1 <= x <= max_x + 1) and (min_y - 1 <= y <= max_y + 1) and (min_z - 1 <= z <= max_z + 1)):
        return

    if (x, y, z) in cubes:
        return

    external_air.add((x, y, z))

    for dx in [-1, 1]:
        find_external_air(x + dx, y, z)

    for dy in [-1, 1]:
        find_external_air(x, y + dy, z)

    for dz in [-1, 1]:
        find_external_air(x, y, z + dz)


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

cubes = set()

for line in lines:
    x, y, z = map(int, line.split(','))
    cubes.add((x, y, z))

min_x = min(x for x, y, z in cubes)
max_x = max(x for x, y, z in cubes)

min_y = min(y for x, y, z in cubes)
max_y = max(y for x, y, z in cubes)

min_z = min(z for x, y, z in cubes)
max_z = max(z for x, y, z in cubes)

external_air = set()

sys.setrecursionlimit(20000)

for x in [min_x - 1, max_x + 1]:
    for y in range(min_y, max_y + 1):
        for z in range(min_z, max_z + 1):
            find_external_air(x, y, z)

for x in range(min_x, max_x + 1):
    for y in [min_y - 1, max_y + 1]:
        for z in range(min_z, max_z + 1):
            find_external_air(x, y, z)

for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        for z in [min_z - 1, max_z + 1]:
            find_external_air(x, y, z)

area = sum(free_sides(*cube) for cube in cubes)
print(area)
