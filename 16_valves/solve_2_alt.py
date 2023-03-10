from dataclasses import dataclass
from collections import deque
from pprint import pprint


def compute_dists(root: str, flow_rate: dict[str, int], leads_to: dict[str, list[str]]) -> dict[str, int]:
    dist_to = {root: 0}
    queue = deque([root])

    while queue:
        parent = queue.popleft()

        for child in leads_to[parent]:
            if child not in dist_to:
                dist_to[child] = dist_to[parent] + 1
                queue.append(child)

    del dist_to[root]

    return {name: dist for name, dist in dist_to.items() if flow_rate[name]}


def compress_graph(flow_rate: dict[str, int], leads_to: dict[str, list[str]], start: str) -> (dict[str, int], dict[str, dict[str, int]], dict[str, int]):
    assert not flow_rate[start]
    new_flow_rate = {name: rate for name, rate in flow_rate.items() if rate}
    dist_to = {}

    for name in new_flow_rate.keys():
        dist_to[name] = compute_dists(name, flow_rate, leads_to)

    return new_flow_rate, dist_to, compute_dists(start, flow_rate, leads_to)


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

flow_rate = {}
leads_to = {}

for line in lines:
    first, second = line.split(';')

    first = first[len('Valve '):]
    valve_name, rate = first.split(' has flow rate=')
    rate = int(rate)

    next_valves = second[len(' tunnels lead to valves '):].split(', ')

    flow_rate[valve_name] = rate
    leads_to[valve_name] = next_valves

start_valve = 'AA'

flow_rate, dist_to, compressed_starts = compress_graph(flow_rate, leads_to, start_valve)

valve_to_id = {name: i for i, name in enumerate(flow_rate.keys())}

flow_rate = {valve_to_id[name]: rate for name, rate in flow_rate.items()}
flow_rate = tuple(flow_rate[i] for i in range(len(flow_rate)))

dist_to = {valve_to_id[parent]: {valve_to_id[child]: dist for child, dist in children.items()} for parent, children in dist_to.items()}
dist_to = tuple(dist_to[i] for i in range(len(dist_to)))

for i, dists in enumerate(dist_to):
    dists[i] = -1

dist_to = tuple(tuple(dists[i] for i in range(len(dists))) for dists in dist_to)

total_minutes = 26

single_states = [set() for _ in range(total_minutes + 1)]

for name, dist in compressed_starts.items():
    single_states[dist].add((valve_to_id[name], 0, 0))

for minute in range(0, total_minutes):
    cur_states = single_states[minute]

    if cur_states:
        best_pressure = max(s[2] for s in cur_states)
    else:
        best_pressure = 0

    print('minute =', minute, 'state count =', len(cur_states), 'best pressure =', best_pressure)

    for cur_valve, opened_valves, pressure in cur_states:
        valve_mask = 1 << cur_valve

        if not (opened_valves & valve_mask):
            new_pressure = pressure + (total_minutes - minute - 1) * flow_rate[cur_valve]
            single_states[minute + 1].add((cur_valve, opened_valves | valve_mask, new_pressure))

        for next_valve, dist in enumerate(dist_to[cur_valve]):
            if dist == -1:
                continue

            if minute + dist <= total_minutes:
                single_states[minute + dist].add((next_valve, opened_valves, pressure))

all_valves_mask = (1 << (len(valve_to_id) + 1)) - 1
best_pressure = 0

for cur_single_states in single_states:
    states_per_open_valves = [[] for _ in range(all_valves_mask + 1)]

    for state in cur_single_states:
        opened_valves = state[1]
        states_per_open_valves[opened_valves].append(state)

    states_per_open_valves = [(mask, states) for mask, states in enumerate(states_per_open_valves) if states]
    best_pressure_per_open_valves = [(mask, max(s[2] for s in states)) for mask, states in states_per_open_valves]

    for first_opened_valves, first_pressure in best_pressure_per_open_valves:
        for second_opened_valves, second_pressure in best_pressure_per_open_valves:
            if not (first_opened_valves & second_opened_valves):
                best_pressure = max(best_pressure, first_pressure + second_pressure)

print(best_pressure)

