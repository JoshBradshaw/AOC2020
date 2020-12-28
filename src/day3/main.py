def traverse_slope(right, down):
    tree_count = 0
    ii, jj = 0, 0
    while jj < len(pattern):
        if pattern[jj][ii] == '#':
            tree_count += 1

        ii = (ii + right) % len(pattern[0])
        jj += down

    return tree_count

pattern = []
with open('input.txt') as f:
    for line in f:
        pattern.append(line.strip())

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
answer = 1
for slope in slopes:
    answer *= traverse_slope(*slope)
print(answer)

