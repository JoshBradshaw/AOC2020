import fileinput
import numpy as np


def part1(schedule, timestamp):
    schedule = [int(n) for n in schedule if not n is 'x']
    departure_delays = [s-(timestamp % s) for s in schedule]
    idx = np.argmin(departure_delays)
    return schedule[idx] * departure_delays[idx]

def part2(schedule):
    constraints = [(int(delay), int(bus_id)) for delay, bus_id in enumerate(schedule) if bus_id != 'x']
    constraints.sort(key=lambda x: x[1], reverse=True)

    def num_constaints_met(n, constraints):
        constraints_met = []
        for delay, bus_id in constraints:
            if (n + delay) % bus_id == 0:
                constraints_met.append(bus_id)
        return constraints_met

    n = constraints[0][1]
    constraints_met = [n]
    while len(constraints_met) != len(constraints):
        n += np.product(constraints_met)
        constraints_met = num_constaints_met(n, constraints)

    return n




def main():
    lines = fileinput.input()
    timestamp = int(next(lines))
    schedule = next(lines).split(',')
    #print(part1(schedule, timestamp))
    print(part2(schedule))

main()