from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class State:
    cur_valves: tuple[int, int]
    valves_opened: int

    @staticmethod
    def make_empty(start_id: int, valves_count: int) -> 'State':
        return State((start_id, start_id), 0)

    def open_valve(self, cur_index: int, flow_rate_id: dict[str, int]) -> Optional['State']:
        valve_id = self.cur_valves[cur_index]

        if (self.valves_opened & (1 << valve_id)) or not flow_rate_id[valve_id]:
            return None

        new_opened = self.valves_opened | (1 << valve_id)

        return State(self.cur_valves, new_opened)

    def move_to(self, cur_index: int, new_valve: int) -> 'State':
        new_cur_valves = self.cur_valves[:cur_index] + (new_valve,) + self.cur_valves[cur_index + 1:]
        return State(new_cur_valves, self.valves_opened)


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

valve_to_id = {valve: i for i, valve in enumerate(flow_rate.keys())}

flow_rate_id = {}

for valve, rate in flow_rate.items():
    flow_rate_id[valve_to_id[valve]] = rate

leads_to_id = {}

for valve, children in leads_to.items():
    leads_to_id[valve_to_id[valve]] = [valve_to_id[v] for v in children]

start_valve = 'AA'

states = {State.make_empty(valve_to_id[start_valve], len(valve_to_id)): 0}

valves_count = len(valve_to_id)
all_open = (1 << (valves_count + 1)) - 1
print('valves count:', valves_count)

simulate_minutes = 26
minute_count = 26

for minute in range(1, simulate_minutes + 1):
    print('minute =', minute - 1, 'state count =', len(states), 'best pressure =', max(states.values()))

    new_states = dict()

    for state, pressure in states.items():
        if state.valves_opened == all_open:
            new_states[state] = pressure
            continue

        if (partial_new_state := state.open_valve(0, flow_rate_id)) is not None:
            partial_new_pressure = pressure + (minute_count - minute) * flow_rate_id[partial_new_state.cur_valves[0]]

            if (new_state := partial_new_state.open_valve(1, flow_rate_id)) is not None:
                new_pressure = partial_new_pressure + (minute_count - minute) * flow_rate_id[new_state.cur_valves[1]]
                new_states[new_state] = max(new_pressure, new_states.get(new_state, 0))

            for next_valve in leads_to_id[state.cur_valves[1]]:
                new_state = partial_new_state.move_to(1, next_valve)
                new_states[new_state] = max(partial_new_pressure, new_states.get(new_state, 0))

        for next_valve_0 in leads_to_id[state.cur_valves[0]]:
            partial_new_state = state.move_to(0, next_valve_0)

            if (new_state := partial_new_state.open_valve(1, flow_rate_id)) is not None:
                new_pressure = pressure + (minute_count - minute) * flow_rate_id[new_state.cur_valves[1]]
                new_states[new_state] = max(new_pressure, new_states.get(new_state, 0))

            for next_valve in leads_to_id[state.cur_valves[1]]:
                new_state = partial_new_state.move_to(1, next_valve)
                new_states[new_state] = max(pressure, new_states.get(new_state, 0))

        del states
        states = new_states

print('best:', max(states.values()))
