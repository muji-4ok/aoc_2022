from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __neg__(self) -> 'Vector':
        return Vector(-self.x, -self.y)

    def __mod__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x % other.x, self.y % other.y)


def in_bounds(point: Vector) -> bool:
    return 0 <= point.x < width and 0 <= point.y < height


def safe_to_move(point: Vector) -> bool:
    return all(-direction not in blizzards[(point + direction) % sizes] for direction in DIRECTIONS)


def calculate_moves(source: Vector, destination: Vector) -> int:
    global blizzards

    dist_to = {source: 0}
    step = 0

    while destination not in dist_to:
        step += 1
        new_dist_to = {}

        for point, dist in dist_to.items():
            for direction in DIRECTIONS_AND_SKIP:
                new_point = point + direction

                if new_point == destination or new_point == source or (in_bounds(new_point) and safe_to_move(new_point)):
                    new_dist_to[new_point] = min(new_dist_to.get(new_point, 99999), dist + 1)

        dist_to = new_dist_to

        new_blizzards = defaultdict(list)

        for point, directions in blizzards.items():
            for direction in directions:
                new_blizzards[(point + direction) % sizes].append(direction)

        blizzards = new_blizzards

        print('step =', step, 'states =', len(dist_to))

    return dist_to[destination]


UP = Vector(0, -1)
DOWN = Vector(0, 1)
LEFT = Vector(-1, 0)
RIGHT = Vector(1, 0)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
DIRECTIONS_AND_SKIP = DIRECTIONS + [Vector(0, 0)]


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

blizzards = defaultdict(list)

for y, line in enumerate(lines[1:-1]):
    for x, c in enumerate(line[1:-1]):
        if c == '.':
            continue

        if c == '>':
            d = RIGHT
        elif c == '<':
            d = LEFT
        elif c == '^':
            d = UP
        else:
            d = DOWN

        blizzards[Vector(x, y)] = [d]

width = len(lines[0]) - 2
height = len(lines) - 2
sizes = Vector(width, height)

start = Vector(0, -1)
end = Vector(width - 1, height)

result = 0
result += calculate_moves(start, end)
result += calculate_moves(end, start)
result += calculate_moves(start, end)

print(result)
