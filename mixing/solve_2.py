def correct_destination(destination: int, length: int) -> int:
    return destination % (length - 1)


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

key = 811589153

values = [int(l) * key for l in lines]
numbered_values = list(enumerate(values))

for _ in range(10):
    for i, v in enumerate(values):
        source = numbered_values.index((i, v))

        value = numbered_values[source][1]

        destination = correct_destination(source + value, len(values))
        numbered_values.insert(destination, numbered_values.pop(source))

        # print('value =', value, 'source =', source, 'want =', destination, 'true =', numbered_values.index((i, v)))

zero_index = numbered_values.index((values.index(0), 0))
target_indices = [(zero_index + offset) % len(values) for offset in [1000, 2000, 3000]]

# print([v[1] for v in numbered_values])
# print(numbered_values)

# print([numbered_values[i][1] for i in target_indices])

print(sum(numbered_values[i][1] for i in target_indices))

