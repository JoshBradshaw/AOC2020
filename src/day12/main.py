import fileinput

CARDINAL_DIR_TO_COMPLEX = {'N': 1, 'S': -1, 'E': 1j, 'W': -1j}

def part1(nav_steps):
    distance = 0 + 0j
    current_orientation = 0 + 1j
    for action, value in nav_steps:
        if action in "NESW":
            distance += CARDINAL_DIR_TO_COMPLEX[action] * value
        elif action in 'LR':
            current_orientation *= (1j if action == 'R' else -1J)**(abs(value) // 90)
        else:
            distance += current_orientation * value
    return int(abs(distance.real) + abs(distance.imag))

def part2(nav_steps):
    waypoint = 1 + 10j
    distance = 0 + 0j
    for action, value in nav_steps:
        if action in "NESW":
            waypoint += CARDINAL_DIR_TO_COMPLEX[action] * value
        elif action in 'LR':
            waypoint *= (1j if action == 'R' else -1j)**(abs(value) // 90)
        else:
            distance += waypoint * value
    return int(abs(distance.real) + abs(distance.imag))

steps = [(d[0], int(d[1:].strip())) for d in fileinput.input()]
print(part1(steps))
print(part2(steps))