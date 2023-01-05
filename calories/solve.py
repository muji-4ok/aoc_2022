import operator
import functools

with open('input.txt') as f:
    per_elf_lines = f.read().split('\n\n')[:-1]

elf_calories = []

for i, elf_lines in enumerate(per_elf_lines):
    elf_calories.append(sum(map(int, elf_lines.split('\n'))))

print(sum(sorted(elf_calories)[-3:]))
