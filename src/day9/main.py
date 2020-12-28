from collections import deque
import fileinput
from itertools import permutations

def part1(nums, preamble_len):
    preamble = deque(nums[:preamble_len], maxlen=preamble_len)
    preamble_permutations = list(permutations(preamble, 2))
    preamble_sum_dequeue = deque([a+b for (a, b) in preamble_permutations], maxlen=len(preamble_permutations))

    for n in nums[preamble_len:]:
        if preamble_sum_dequeue.count(n) == 0:
            return n
        preamble.append(n)
        new_permutations = (p for (p, _) in zip(permutations(reversed(preamble), 2), range(preamble_len-1)))
        preamble_sum_dequeue.extend(a+b for a, b in new_permutations)

def part2(nums, target):
    s = l = h = 0
    while s != target or h-l < 2:
        if s < target:
            s += nums[h]
            h += 1
        else:
            s -= nums[l]
            l += 1
    return min(nums[l:h]) + max(nums[l:h])


nums = map(int, fileinput.input())
p1_ans = part1(nums, preamble_len=25)
print(p1_ans)
print(part2(nums, target=p1_ans))