import numpy as np

def part2(cup_labels, n_cups, n_rounds, max_cup_value):
    next_cup_lookup = np.zeros(max_cup_value+1, dtype=np.int)
    for ii in range(n_cups):
        next_cup_lookup[cup_labels[ii]] = cup_labels[(ii+1) % n_cups]

    current_cup_label = cup_labels[0]
    for ii in range(n_rounds):
        print(ii)

        cups_picked_up = []
        tmp_cup = current_cup_label
        for _ in range(3):
            tmp_cup = next_cup_lookup[tmp_cup]
            cups_picked_up.append(tmp_cup)

        next_cup_lookup[current_cup_label] = next_cup_lookup[tmp_cup]

        dest_cup_label = current_cup_label -1
        while dest_cup_label in cups_picked_up or dest_cup_label < 1:
            if dest_cup_label < 1:
                dest_cup_label = max_cup_value
            else:
                dest_cup_label -= 1

        tmp_cup = next_cup_lookup[dest_cup_label]
        next_cup_lookup[dest_cup_label] = cups_picked_up[0]
        next_cup_lookup[cups_picked_up[2]] = tmp_cup

        current_cup_label = next_cup_lookup[current_cup_label]

    # part 1
    answer = []
    current_cup = 1
    for _ in range(n_cups-1):
        current_cup = next_cup_lookup[current_cup]
        answer.append(current_cup)

    # part 2
    ans1 = next_cup_lookup[1]
    ans2 = next_cup_lookup[ans1]

    return ans1 * ans2, "".join(f"{n}" for n in ans)



puzzle_input = "614752839"
n_cups = 1000000

cup_labels = [int(n) for n in puzzle_input]
for n in range(max(cup_labels)+1, n_cups + 1):
    cup_labels.append(n)

print(part2(cup_labels, len(cup_labels), 10*n_cups, max(cup_labels)))
