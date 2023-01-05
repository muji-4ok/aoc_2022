from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def dist(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def parse_point(s: str) -> Point:
    x, y = s.split(', ')
    x = int(x.lstrip('x='))
    y = int(y.lstrip('y='))
    return Point(x, y)


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

target_y = 2000000
empty_xs = set()

for sensor, beacon in sensors_and_beacons:
    beacon_dist = dist(sensor, beacon)

    x = sensor.x

    while True:
        p = Point(x, target_y)

        if dist(p, sensor) > beacon_dist:
            break

        if p not in beacons_set:
            empty_xs.add(x)

        x += 1

    x = sensor.x

    while True:
        p = Point(x, target_y)

        if dist(p, sensor) > beacon_dist:
            break

        if p not in beacons_set:
            empty_xs.add(x)

        x -= 1

print(len(empty_xs))

