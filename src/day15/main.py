import fileinput
from collections import defaultdict

def part1(numbers):
    turn_last_spoken = defaultdict(list)
    turn_last_spoken.update({n: [ii] for (ii, n) in enumerate(numbers)})

    last_number_spoken = numbers[-1]
    for turn in range(len(numbers), 30000000):
        if len(turn_last_spoken[last_number_spoken]) == 1:
            last_number_spoken = 0
        else:
            last_number_spoken = turn_last_spoken[last_number_spoken][-1] - turn_last_spoken[last_number_spoken][-2]

        turn_last_spoken[last_number_spoken].append(turn)
    return last_number_spoken

numbers = [int(n) for n in next(fileinput.input()).split(',')]
print(part1(numbers))