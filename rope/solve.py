def move_tail(head_x: int, head_y: int, tail_x: int, tail_y: int) -> (int, int):
    dx = head_x - tail_x
    dy = head_y - tail_y

    if dx == 0 and abs(dy) >= 2:
        dy = 1 if dy > 0 else -1
    elif dy == 0 and abs(dx) >= 2:
        dx = 1 if dx > 0 else -1
    elif abs(dx) + abs(dy) >= 3:
        dx = 1 if dx > 0 else -1
        dy = 1 if dy > 0 else -1
    else:
        dx = 0
        dy = 0

    return tail_x + dx, tail_y + dy


letter_to_dir = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}

with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

head_x = 0
head_y = 0
tail_x = 0
tail_y = 0

points_visited = set([(tail_x, tail_y)])

for line in lines:
    letter, count = line.split()
    count = int(count)
    dx, dy = letter_to_dir[letter]

    for _ in range(count):
        head_x += dx
        head_y += dy
        #print('head', head_x, head_y)
        tail_x, tail_y = move_tail(head_x, head_y, tail_x, tail_y)
        #print('tail', tail_x, tail_y)
        #print('diff', head_x - tail_x, head_y - tail_y)
        points_visited.add((tail_x, tail_y))

#print(points_visited)
print(len(points_visited))

