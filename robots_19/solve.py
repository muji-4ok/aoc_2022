from dataclasses import dataclass
from functools import cache
from typing import Optional


@dataclass(unsafe_hash=False)
class Materials:
    # { material -> count }
    d: dict[str, int]

    def __hash__(self) -> int:
        return hash((self.d['ore'], self.d['clay'], self.d['obsidian'], self.d['geode']))


@dataclass(unsafe_hash=False)
class Blueprint:
    # { name -> material costs }
    robots: dict[str, Materials]

    @staticmethod
    def mine(robots: Materials, materials: Materials) -> Materials:
        new_materials_d = materials.d.copy()

        for material, count in robots.d.items():
            new_materials_d[material] += count

        return Materials(new_materials_d)

    def try_build_robot(self, robot_name: str, need_materials: Materials, materials: Materials, active_robots: Materials) -> Optional[tuple[Materials, Materials]]:
        if all(materials.d[name] >= count for name, count in need_materials.d.items()):
            new_materials_d = materials.d.copy()
            new_active_robots_d = active_robots.d.copy()

            for name, count in need_materials.d.items():
                new_materials_d[name] -= count

            new_active_robots_d[robot_name] += 1

            return Materials(new_active_robots_d), Materials(new_materials_d)
        else:
            return None

    @cache
    def simulate(self, minutes: int, active_robots: Materials, materials: Materials) -> Materials:
        print(minutes)

        if not minutes:
            return materials

        possible = []

        for new_robot, need_materials in self.robots.items():
            if (result := self.try_build_robot(new_robot, need_materials, materials, active_robots)) is not None:
                new_active_robots, new_materials = result
                new_materials = self.mine(active_robots, new_materials)
                possible.append(self.simulate(minutes - 1, new_active_robots, new_materials))

        possible.append(self.simulate(minutes - 1, active_robots, self.mine(active_robots, materials)))

        return max(possible, key=lambda m: m.d['geode'])

    def __hash__(self) -> int:
        return hash((hash(self.robots['ore']), hash(self.robots['clay']), hash(self.robots['obsidian']), hash(self.robots['geode'])))


with open('sample_input.txt') as f:
    lines = f.read().split('\n')[:-2]

blueprints = []

for line in lines:
    first, second = line.split(': ')
    robots = [s[len('Each '):].strip() for s in second.split('.')[:-1]]

    blueprint = Blueprint({})

    for robot in robots:
        first, second = robot.split(' robot costs ')
        name = first
        materials = second.split(' and ')
        materials = [m.split() for m in materials]
        materials = {material: int(count) for count, material in materials}

        for material in ['ore', 'clay', 'obsidian', 'geode']:
            if material not in materials:
                materials[material] = 0

        blueprint.robots[name] = Materials(materials)

    blueprints.append(blueprint)

total_minutes = 24
starting_materials = Materials({'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0})
starting_robots = Materials({'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0})

for blueprint in blueprints:
    print(blueprint.simulate(total_minutes, starting_robots, starting_materials))

