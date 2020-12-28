import fileinput
import re
from collections import defaultdict

rule_names = []
rules = []
ticket = []
other_tickets = []

lines = fileinput.input()
for line in lines:
    if ': ' in line:
        rule_regex = r'(\d+)-(\d+)'
        rule_names.append(line.split(':')[0])
        rules.append([(int(lo), int(hi)) for lo, hi in re.findall(rule_regex, line)])
    elif 'your ticket' in line:
        ticket = [int(n) for n in next(lines).strip().split(',')]
    elif line[0].isdigit():
        other_tickets.append([int(n) for n in line.strip().split(',')])
    else:
        pass

def part1(other_tickets, rules):
    invalid_values = 0
    for ticket in other_tickets:
        for val in ticket:
            if not any(lo <= val <= hi for lo, hi in rules):
                invalid_values += val
    return invalid_values

def part2(your_ticket, other_tickets, rule_names, rules):
    valid_tickets = []

    for tk in other_tickets:
        if all(any(any(lo <= val <= hi for lo, hi in rl) for rl in rules) for val in tk):
            valid_tickets.append(tk)


    rule_column_sets = defaultdict(set)
    for rule_name, rule in zip(rule_names, rules):
        for column in range(len(ticket)):
            if all(any(lo <= tk[column] <= hi for lo, hi in rule) for tk in valid_tickets):
                rule_column_sets[rule_name].add(column)

    for cs in sorted(rule_column_sets.values(), key=len):
        for os in rule_column_sets.values():
            if os > cs:
                os -= cs

    prod = 1
    for rule_name, cs in rule_column_sets.items():
        if 'departure' in rule_name:
            prod *= your_ticket[list(cs)[0]]
    return prod




#print(part1(other_tickets, rules))
print(part2(ticket, other_tickets, rule_names, rules))
