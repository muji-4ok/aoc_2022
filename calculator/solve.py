def compute(name: str) -> int:
    op = operations[name]

    if isinstance(op, int):
        return op

    result = eval(op, globals(), {dep: compute(dep) for dep in dependencies[name]})
    operations[name] = result

    return result


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

print(compute('root'))

