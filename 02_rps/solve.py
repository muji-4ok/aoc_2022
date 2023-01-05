letters_to_shape_cost = {
    'A': 1, # Rock
    'B': 2, # Paper
    'C': 3, # Scissors
    'X': 1,
    'Y': 2,
    'Z': 3,
}

# opponent, me
outcome_table = {
    (1, 1): 3,
    (2, 2): 3,
    (3, 3): 3,
    (1, 2): 6,
    (2, 3): 6,
    (3, 1): 6,
    (2, 1): 0,
    (3, 2): 0,
    (1, 3): 0,
}

with open('sample_input.txt') as f:
    lines = f.read().split('\n')[:-2]

result = 0

for line in lines:
    opponent, me = map(lambda x: letters_to_shape_cost[x], line.split())
    result += me + outcome_table[(opponent, me)]

print(result)
