import string


def char_to_priority(c: str) -> int:
    return string.ascii_letters.find(c) + 1


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

result = 0

for l1, l2, l3 in zip(lines[::3], lines[1::3], lines[2::3]):
    s1, s2, s3 = map(set, [l1, l2, l3])
    s = s1 & s2 & s3
    assert len(s) == 1
    result += char_to_priority(s.pop())

print(result)

