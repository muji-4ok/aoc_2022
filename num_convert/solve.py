snafu_to_decimal_digits = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

decimal_to_snafu_digits = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2',
}

decimal_to_carry_ret = {
    -5: (-1, 0),
    -4: (-1, 1),
    -3: (-1, 2),
    -2: (0, -2),
    -1: (0, -1),
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, -2),
    4: (1, -1),
    5: (1, 0),
}


def snafu_to_decimal(s: str) -> int:
    base = 1
    result = 0

    for digit in reversed(s):
        result += base * snafu_to_decimal_digits[digit]
        base *= 5

    return result


def sum_snafu(s1: str, s2: str) -> str:
    carry = 0
    result = ''

    max_len = max(len(s1), len(s2)) + 1
    s1 = s1.rjust(max_len, '0')
    s2 = s2.rjust(max_len, '0')

    for d1, d2 in zip(reversed(s1), reversed(s2)):
        i1 = snafu_to_decimal_digits[d1]
        i2 = snafu_to_decimal_digits[d2]
        next_carry, ret = decimal_to_carry_ret[i1 + i2 + carry]
        carry = next_carry
        result += decimal_to_snafu_digits[ret]

    result = result.rstrip('0')

    if not result:
        return '0'
    else:
        return ''.join(reversed(result))


with open('input.txt') as f:
    lines = f.read().split('\n')

result = '0'

for line in lines:
    result = sum_snafu(result, line)

print(result)
print(snafu_to_decimal(result))
