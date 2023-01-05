from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class State:
    cur_valves: tuple[str, str]
    valves_opened: tuple[bool]
    pressure: int

    @staticmethod
    def make_empty(start: str, valves_count: int) -> 'State':
        return State((start, start), tuple(False for _ in range(valves_count)), 0)

    def open_valve(self, cur_index: int, flow_rate: dict[str, int], valve_to_id: dict[str, int], minutes_will_pass: int) -> Optional['State']:
        cur_valve = self.cur_valves[cur_index]
        valve_id = valve_to_id[cur_valve]

        if self.valves_opened[valve_id] or not flow_rate[cur_valve]:
            return None

        new_opened = self.valves_opened[:valve_id] + (True,) + self.valves_opened[valve_id + 1:]
        new_pressure = self.pressure + minutes_will_pass * flow_rate[cur_valve]

        return State(self.cur_valves, new_opened, new_pressure)

    def move_to(self, cur_index: int, new_valve: str) -> 'State':
        new_cur_valves = self.cur_valves[:cur_index] + (new_valve,) + self.cur_valves[cur_index + 1:]
        return State(new_cur_valves, self.valves_opened, self.pressure)


with open('sample_input.txt') as f:
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

valve_to_id = {valve: i for i, valve in enumerate(flow_rate.keys())}
id_to_valve = {i: valve for i, valve in enumerate(flow_rate.keys())}

start_valve = 'AA'

states = {State.make_empty(start_valve, len(valve_to_id))}

print('valves count:', len(valve_to_id))

simulate_minutes = 30
minute_count = 30

for minute in range(1, simulate_minutes + 1):
    print('minute =', minute - 1, 'state count =', len(states), 'best pressure =', max(s.pressure for s in states))

    new_states = set()

    for state in states:
        if (new_state := state.open_valve(0, flow_rate, valve_to_id, minute_count - minute)) is not None:
            new_states.add(new_state)

        for next_valve in leads_to[state.cur_valves[0]]:
            new_states.add(state.move_to(0, next_valve))

        del states
        states = new_states

print('best:', max(s.pressure for s in states))
