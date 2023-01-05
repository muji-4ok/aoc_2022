import string


def char_to_priority(c: str) -> int:
    return string.ascii_letters.find(c) + 1


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

result = 0

for line in lines:
    assert len(line) % 2 == 0

    first, second = line[:len(line) // 2], line[len(line) // 2:]

    assert len(first) == len(second)

    first = set(first)
    second = set(second)
    both = first & second

    assert len(both) == 1

    letter = both.pop()

    result += char_to_priority(letter)

print(result)


