import operator

from functools import reduce
from typing import Optional


def try_compute(name: str) -> Optional[int]:
    op = operations[name]

    if name == 'humn':
        return None

    if isinstance(op, int):
        return op

    computed = {dep: try_compute(dep) for dep in dependencies[name]}

    if None in computed.values():
        return None

    result = eval(op, globals(), computed)
    operations[name] = result

    return result


def solve_operation(op: str, known_name: str, known_value: int, result: int) -> int:
    first, op, second = op.split()

    if op == '+':
        return result - known_value
    elif op == '-':
        if known_name == first:
            return known_value - result
        else:
            return known_value + result
    elif op == '*':
        return result // known_value
    elif op == '//':
        if known_name == first:
            return known_value // result
        else:
            return known_value * result
    else:
        assert False


def solve_for_humn(start: str, want: int) -> int:
    if start == 'humn':
        return want

    op = operations[start]
    deps = dependencies[start]
    print(start, op, deps)
    computed = [try_compute(dep) for dep in deps]

    if computed[0] is None:
        known_name = deps[1]
        known_value = computed[1]

        unknown_name = deps[0]
    elif computed[1] is None:
        known_name = deps[0]
        known_value = computed[0]

        unknown_name = deps[1]
    else:
        assert False

    need = solve_operation(op, known_name, known_value, want)

    return solve_for_humn(unknown_name, need)


def full_dependencies(name: str) -> list[str]:
    return [name] + reduce(operator.add, map(full_dependencies, dependencies[name]), [])


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

operations = {}
dependencies = {}

for line in lines:
    name, operation = line.split(': ')
    operation = operation.replace('/', '//')
    parts = operation.split()

    if len(parts) == 1:
        operations[name] = int(operation)
        dependencies[name] = []
    else:
        operations[name] = operation
        dependencies[name] = [parts[0], parts[2]]

left = full_dependencies(dependencies['root'][0])
right = full_dependencies(dependencies['root'][1])

if 'humn' in left:
    dynamic, static = left, right
else:
    dynamic, static = right, left

need = try_compute(static[0])
assert need is not None
print(need)

assert solve_operation('a + x', 'a', 3, 5) == 2
assert solve_operation('x + a', 'a', 3, 5) == 2
assert solve_operation('a - x', 'a', 5, 3) == 2
assert solve_operation('x - a', 'a', 3, 5) == 8
assert solve_operation('a * x', 'a', 7, 21) == 3
assert solve_operation('x * a', 'a', 3, 21) == 7
assert solve_operation('a // x', 'a', 21, 3) == 7
assert solve_operation('x // a', 'a', 3, 7) == 21

print(solve_for_humn(dynamic[0], need))
