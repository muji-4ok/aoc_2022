with open('input.txt') as f:
    configuration, moves = f.read().split('\n\n')

configuration_lines = configuration.split('\n')
stacks_count = len(configuration_lines[-1].split())
configuration_lines = configuration_lines[:-1]

stacks = [[] for _ in range(stacks_count)]

for line in reversed(configuration_lines):
    for i, start in enumerate(range(0, len(line), 4)):
        crate = line[start:start+3]

        if crate[0] == '[':
            stacks[i].append(crate[1])

moves_lines = moves.split('\n')[:-1]

for line in moves_lines:
    parts = line.split()
    count = int(parts[1])
    source = int(parts[3]) - 1
    destination = int(parts[5]) - 1

    for _ in range(count):
        stacks[destination].append(stacks[source].pop())

print(*[s[-1] for s in stacks], sep='')

