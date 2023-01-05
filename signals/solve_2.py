with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

output = [[]]
x = 1
row_position = 0

for line in lines:
    if row_position == 40:
        output.append([])
        row_position = 0

    output[-1].append('#' if abs(row_position - x) <= 1 else '.')

    if line == 'noop':
        row_position += 1
    else:
        command, num = line.split()
        num = int(num)
        assert command == 'addx'

        row_position += 1

        if row_position == 40:
            output.append([])
            row_position = 0

        output[-1].append('#' if abs(row_position - x) <= 1 else '.')

        x += num
        row_position += 1

print('\n'.join(map(lambda l: ''.join(l), output)))
