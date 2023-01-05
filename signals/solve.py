with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

cycle = 1
times = [20, 60, 100, 140, 180, 220]
strengths = []
x = 1

for line in lines:
    if line == 'noop':
        cycle += 1
    else:
        # print(line)
        command, num = line.split()
        num = int(num)
        assert command == 'addx'

        if cycle + 1 in times:
            # print('Calculating for', cycle + 1)
            strengths.append((cycle + 1) * x)

        # print('Add', num)
        x += num
        cycle += 2

    if cycle in times:
        # print('Calculating for', cycle)
        strengths.append(cycle * x)

print(sum(strengths))
