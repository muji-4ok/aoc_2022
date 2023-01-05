letters_to_shape_cost = {
    'A': 1, # Rock
    'B': 2, # Paper
    'C': 3, # Scissors
}

letters_to_outcome_cost = {
    'X': 0, # Lose
    'Y': 3, # Draw
    'Z': 6, # Win
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

with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

result = 0

for line in lines:
    opponent, outcome = line.split()

    opponent = letters_to_shape_cost[opponent]
    outcome = letters_to_outcome_cost[outcome]

    for me in range(1, 4):
        if outcome_table[(opponent, me)] == outcome:
            result += me + outcome
            break

print(result)
