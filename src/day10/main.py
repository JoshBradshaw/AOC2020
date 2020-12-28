from collections import Counter
import fileinput
from functools import lru_cache
import numpy as np


def part1(jolts):
    diffs = Counter(b - a for a, b in zip(jolts, jolts[1:]))
    diff_counts = Counter(diffs)
    return diff_counts[1] * diff_counts[3]


def part2(adapter_ratings, rating_index):
    @lru_cache(maxsize=None)
    def p2(index):
        if index == 0:
            return 1
        else:
            combinations = 0
            for ii in [-1, -2, -3]:
                diff = adapter_ratings[index] - adapter_ratings[index + ii]
                if index + ii >= 0 and diff <= 3:
                    combinations += p2(index + ii)
            return combinations
    return p2(rating_index)


def part2_pretty(jolts):
    @lru_cache(maxsize=None)
    def ways(idx):
        return (1 if idx == len(jolts) - 1
                else sum(ways(n) for n, x in enumerate(jolts[idx+1:idx+4], start=idx+1) if x <= jolts[idx]+3))
    return ways(0)


def part2_iterative(jolt_ratings):
    ways = np.zeros(max(jolt_ratings)+1, dtype=int)
    ways[0] = 1
    for rating in jolt_ratings[1:]:
        ways[rating] = ways[rating-3] + ways[rating-2] + ways[rating-1]
    return ways[-1]

jolts = list(map(int, fileinput.input()))
jolts.append(0)
jolts.sort()
jolts.append(jolts[-1] + 3)
#print(part2_pretty(jolts))
print(part2_iterative(jolts))
