from collections import Counter

# part 1
with open('input.txt') as f:
    data = f.read()
    groups = data.split('\n\n')

    total = 0
    for group in groups:
        people_count = group.count('\n') + 1
        answer_count = len(set(c for c in group if c.isalpha()))
        total += answer_count

# part 2
with open('input.txt') as f:
    data = f.read()
    groups = data.split('\n\n')

    total = 0
    for group in groups:
        people_count = group.count('\n') + 1
        answer_count = Counter(c for c in group if c.isalpha())

        for ans, count in answer_count.items():
            if count == people_count:
                total += 1

print(total)