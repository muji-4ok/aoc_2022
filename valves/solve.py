from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class State:
    cur_valve: str
    valves_opened: tuple[bool]
    pressure: int

    @staticmethod
    def make_empty(start: str, valves_count: int) -> 'State':
        return State(start, tuple(False for _ in range(valves_count)), 0)


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
id_to_valve = {i: valve for i, valve in enumerate(flow_rate.keys())}

start_valve = 'AA'

states = {State.make_empty(start_valve, len(valve_to_id))}

print('valves count:', len(valve_to_id))

simulate_minutes = 30
minute_count = 30

for minute in range(1, simulate_minutes + 1):
    last_minute = minute - 1

    print('minute =', last_minute, 'state count =', len(states), 'best pressure =', max(s.pressure for s in states))

    new_states = set()

    for state in states:
        if not state.valves_opened[valve_to_id[state.cur_valve]] and flow_rate[state.cur_valve]:
            valve_id = valve_to_id[state.cur_valve]
            new_opened = state.valves_opened[:valve_id] + (True,) + state.valves_opened[valve_id + 1:]
            new_pressure = state.pressure + (minute_count - minute) * flow_rate[state.cur_valve]

            new_state = State(state.cur_valve, new_opened, new_pressure)

            new_states.add(new_state)

        for next_valve in leads_to[state.cur_valve]:
            new_state = State(next_valve, state.valves_opened, state.pressure)

            new_states.add(new_state)

        del states
        states = new_states

print('best:', max(s.pressure for s in states))
