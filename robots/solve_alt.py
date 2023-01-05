with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

material_to_id = {'ore': 0, 'clay': 1, 'obsidian': 2, 'geode': 3}
id_to_material = {0: 'ore', 1: 'clay', 2: 'obsidian', 3: 'geode'}

blueprints = []

for line in lines:
    first, second = line.split(': ')
    robots = [s[len('Each '):].strip() for s in second.split('.')[:-1]]

    blueprint = {}

    for robot in robots:
        first, second = robot.split(' robot costs ')
        name = first
        materials = second.split(' and ')
        materials = [m.split() for m in materials]
        materials = {material: int(count) for count, material in materials}

        need_materials = [0 for _ in range(len(material_to_id))]

        for material, count in materials.items():
            need_materials[material_to_id[material]] = count

        blueprint[name] = tuple(need_materials)

    blueprints.append(tuple(blueprint[id_to_material[i]] for i in range(len(material_to_id))))

total_minutes = 24
starting_robots = (1, 0, 0, 0)
starting_materials = (0, 0, 0, 0)
starting_state = (starting_robots, starting_materials)

result = 0

for blueprint_id, blueprint in enumerate(blueprints, start=1):
    max_need_robots = [max(blueprint[i][j] for i in range(len(blueprint))) for j in range(len(starting_materials))]
    max_need_robots[-1] = 9999 # don't limit geode robots
    max_need_robots = tuple(max_need_robots)

    states = set([starting_state])

    for minute in range(1, total_minutes + 1):
        new_states = set()

        for robots, materials in states:
            new_materials = list(materials)

            for robot_index, count in enumerate(robots):
                new_materials[robot_index] += count

            possible = set()

            max_possibilities = 0

            for robot_index, need_materials in enumerate(blueprint):
                if robots[robot_index] < max_need_robots[robot_index]:
                    max_possibilities += 1
                else:
                    continue

                if all(have >= need for have, need in zip(materials, need_materials)):
                    new_robots = list(robots)
                    new_robot_materials = new_materials.copy()

                    for material_index, count in enumerate(need_materials):
                        new_robot_materials[material_index] -= count

                    new_robots[robot_index] += 1

                    possible.add((tuple(new_robots), tuple(new_robot_materials)))

            if len(possible) < max_possibilities:
                possible.add((robots, tuple(new_materials)))

            new_states |= possible

        del states
        states = new_states

        print('blueprint =', blueprint_id, 'minute =', minute, 'count =', len(states), 'best =', max(s[1][-1] for s in states))

    max_geodes = max(s[1][-1] for s in states)
    result += blueprint_id * max_geodes

print(result)

