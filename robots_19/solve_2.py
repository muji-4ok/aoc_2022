def pack_to_int(v0: int, v1: int, v2: int, v3: int) -> int:
    return v0 | (v1 << bit_count) | (v2 << (bit_count * 2)) | (v3 << (bit_count * 3))


def set_packed(packed: int, index: int, value: int) -> int:
    return (packed & ~(((1 << bit_count) - 1) << (bit_count * index))) | (value << (bit_count * index))


def get_packed(packed: int, index: int) -> int:
    return (packed & (((1 << bit_count) - 1) << (bit_count * index))) >> (bit_count * index)


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

total_minutes = 32

bit_count = (total_minutes ** 2).bit_length()

starting_robots = pack_to_int(1, 0, 0, 0)
starting_materials = pack_to_int(0, 0, 0, 0)
starting_state = (starting_robots, starting_materials)

best_geodes = []

for blueprint_id, blueprint in enumerate(blueprints[:3], start=1):
    max_need_robots = [max(blueprint[i][j] for i in range(len(blueprint))) for j in range(4)]
    max_need_robots[-1] = 9999 # don't limit geode robots
    max_need_robots = tuple(max_need_robots)

    states = set([starting_state])

    for minute in range(1, total_minutes + 1):
        new_states = set()

        for robots, materials in states:
            new_materials = materials

            for robot_index in range(4):
                count = get_packed(robots, robot_index)
                new_materials = set_packed(new_materials, robot_index, get_packed(new_materials, robot_index) + count)

            possible = set()

            max_possibilities = 0

            for robot_index, need_materials in enumerate(blueprint):
                if get_packed(robots, robot_index) < max_need_robots[robot_index]:
                    max_possibilities += 1
                else:
                    continue

                if all(get_packed(materials, i) >= need_materials[i] for i in range(4)):
                    new_robot_materials = new_materials

                    for material_index, count in enumerate(need_materials):
                        new_robot_materials = set_packed(new_robot_materials, material_index, get_packed(new_robot_materials, material_index) - count)

                    new_robots = set_packed(robots, robot_index, get_packed(robots, robot_index) + 1)

                    possible.add((new_robots, new_robot_materials))

            if len(possible) < max_possibilities:
                possible.add((robots, new_materials))

            new_states |= possible

        del states
        states = new_states

        print('blueprint =', blueprint_id, 'minute =', minute, 'count =', len(states), 'best =', max(get_packed(s[1], 3) for s in states))

    max_geodes = max(get_packed(s[1], 3) for s in states)
    best_geodes.append(max_geodes)

print(best_geodes[0] * best_geodes[1] * best_geodes[2])

