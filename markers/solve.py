with open('input.txt') as f:
    data = f.read().strip()

for end in range(14, len(data)):
    start = end - 14
    substr = data[start:end]

    if len(set(substr)) == 14:
        print(end)
        break

