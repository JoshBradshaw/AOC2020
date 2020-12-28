import fileinput
import re
from functools import lru_cache

def rules_to_regex(rules):
    @lru_cache(maxsize=None)
    def to_regex(rule_idx):
        current_rule = rules[rule_idx]
        if isinstance(current_rule, str):
            return current_rule
        else:
            alternative_rules = []
            for rule_group in current_rule:
                alternative_rules.append("".join(to_regex(subrule) for subrule in rule_group))
            if len(alternative_rules) == 1:
                return "".join(alternative_rules)
            else:
                return "({})".format('|'.join(alternative_rules))
    return to_regex(0)

def part1(rules, messages):
    rule_regex = re.compile(rules_to_regex(rules))
    return sum(1 for message in messages if rule_regex.fullmatch(message))

def part2(rules, messages):
    """
    8: 42 | 42 8
    11: 42 31 | 42 11 31
    :param rules:
    :param messages:
    :return:
    """

    rules[8] = [[42], [42, 42], [42, 42, 42], [42, 42, 42, 42], [42, 42, 42, 42, 42], [42, 42, 42, 42, 42, 42]]
    rules[11] = [[42, 31], [42, 42, 31, 31], [42, 42, 42, 31, 31, 31], [42, 42, 42, 42, 31, 31, 31, 31]]

    rule_regex = re.compile(rules_to_regex(rules))
    return sum(1 for message in messages if rule_regex.fullmatch(message))


rule_lines = []
messages = []

for line in fileinput.input():
    if line[0].isdigit():
        rule_lines.append(line.strip())
    elif not line.strip():
        continue
    else:
        messages.append(line.strip())

rule_lines.sort(key=lambda s: int(s.split(':')[0]))

rules = []
for line in rule_lines:
    rule = line.split(':')[1]
    if '"' in rule:
        rules.append(rule.strip('\n "'))
    else:
        rules.append([list(map(int, subrule.split())) for subrule in rule.split('|')])


print(part1(rules, messages))
print(part2(rules, messages))