from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(order=True)
class Divider:
    x: int
    is_start: bool
    n: int


def dist(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def parse_point(s: str) -> Point:
    x, y = s.split(', ')
    x = int(x.lstrip('x='))
    y = int(y.lstrip('y='))
    return Point(x, y)


def find_x_divider(min_x: int, max_x: int, y: int, sensor: Point, target_dist: int, *, decreasing: bool = False) -> int:
    while max_x - min_x >= 1:
        x = (max_x + min_x) // 2
        p = Point(x, y)
        d = dist(p, sensor)

        if d == target_dist:
            return x
        elif (d > target_dist) ^ (not decreasing):
            min_x = x + 1
        elif (d < target_dist) ^ (not decreasing):
            max_x = x
        else:
            assert False

    return min_x


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

sensors_and_beacons = []
beacons_set = set()

for line in lines:
    first, second = line.split(':')

    first = first.strip().lstrip('Sensor at ')
    second = second.strip().lstrip('closest beacon is at ')

    sensor, beacon = map(parse_point, [first, second])

    sensors_and_beacons.append((sensor, beacon))

    beacons_set.add(beacon)

min_y = 0
max_y = 4000000

for target_y in range(min_y, max_y + 1):
    dividers = []

    for i, (sensor, beacon) in enumerate(sensors_and_beacons):
        beacon_dist = dist(sensor, beacon)

        min_x = sensor.x - beacon_dist
        max_x = sensor.x + beacon_dist

        if dist(sensor, Point(sensor.x, target_y)) <= beacon_dist:
            div_left = find_x_divider(min_x, sensor.x, target_y, sensor, beacon_dist, decreasing=True)
            div_right = find_x_divider(sensor.x, max_x, target_y, sensor, beacon_dist)

            # empty_left = div_left - 1
            # empty_right = div_right + 1

            # print(empty_left, empty_right, target_y, sensor, beacon, beacon_dist)
            # print(div_left, div_right, target_y, sensor, beacon, beacon_dist)

            # dividers.append(Divider(empty_left, i))
            # dividers.append(Divider(empty_right, i))
            dividers.append(Divider(div_left, True, i))
            dividers.append(Divider(div_right, False, i))

    dividers.sort(key=lambda d: d.x)

    open_nums = set()
    last_closed_x = None

    if dividers[0].x > min_y:
        print(dividers[0].x, target_y)
        exit(0)

    if dividers[-1].x < max_y:
        print(dividers[-1].x, target_y)
        exit(0)

    # print(*[str(d.x) + ('s' if d.is_start else 'e') + str(d.n) for d in dividers])

    for i, d in enumerate(dividers):
        if d.n in open_nums:
            open_nums.remove(d.n)

            if not open_nums:
                last_closed_x = d.x
        else:
            open_nums.add(d.n)

            if len(open_nums) == 1 and last_closed_x is not None and d.x - last_closed_x >= 2:
                x = (d.x + last_closed_x) // 2
                # print(d.x - last_closed_x)
                # print(last_closed_x, d.x)
                print(x, target_y)
                assert d.x - last_closed_x == 2
                exit(0)

    if (target_y + 1) % 10000 == 0:
        print(target_y)

