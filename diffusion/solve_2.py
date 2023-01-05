from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)


N = Vector(0, -1)
S = Vector(0, 1)
W = Vector(-1, 0)
E = Vector(1, 0)

ADJACENT_TO = {
    N: [N, N + E, N + W],
    S: [S, S + E, S + W],
    W: [W, N + W, S + W],
    E: [E, N + E, S + E],
}

ALL_ADJACENT = [N, N + E, E, E + S, S, S + W, W, W + N]


def calculate_sizes() -> (int, int):
    xs = [v.x for v in elves]
    ys = [v.y for v in elves]
    return max(ys) - min(ys) + 1, max(xs) - min(xs) + 1


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

elves = set()

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '#':
            elves.add(Vector(x, y))

directions = [N, S, W, E]
round_num = 0

while True:
    round_num += 1
    want_to_move = defaultdict(list)

    for elf in elves:
        if all((elf + adjacent) not in elves for adjacent in ALL_ADJACENT):
            continue

        for direction in directions:
            if all((elf + adjacent) not in elves for adjacent in ADJACENT_TO[direction]):
                want_to_move[elf + direction].append(elf)
                break

    if not want_to_move:
        break

    new_elves = elves.copy()

    for position, wanting_elves in want_to_move.items():
        if len(wanting_elves) == 1:
            old_position = wanting_elves[0]
            new_elves.remove(old_position)
            new_elves.add(position)

    directions = directions[1:] + directions[:1]

    assert len(elves) == len(new_elves)

    elves = new_elves

print(round_num)

