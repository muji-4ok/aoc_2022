def free_sides(x: int, y: int, z: int, cubes: set[tuple[int, int, int]]) -> int:
    result = 6

    for dx in [-1, 1]:
        if (x + dx, y, z) in cubes:
            result -= 1

    for dy in [-1, 1]:
        if (x, y + dy, z) in cubes:
            result -= 1

    for dz in [-1, 1]:
        if (x, y, z + dz) in cubes:
            result -= 1

    return result


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

cubes = set()

for line in lines:
    x, y, z = map(int, line.split(','))
    cubes.add((x, y, z))

area = sum(free_sides(*cube, cubes) for cube in cubes)
print(area)

