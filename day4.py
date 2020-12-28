import re

with open('input.txt') as f:
    data = f.read()

fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']  # , 'cid']
validation_rules = {
    'byr': (r'\d+', lambda byr: 1920 <= int(byr) <= 2002),
    'iyr': (r'\d+', lambda iyr: 2010 <= int(iyr) <= 2020),
    'eyr': (r'\d+', lambda eyr: 2020 <= int(eyr) <= 2030),
    'hgt': (r'\d+(cm|in)', lambda hgt: 150 <= int(hgt.strip('cm')) <= 193 if 'cm' in hgt else 59 <= int(hgt.strip('in')) <= 76),
    'hcl': (r'#[0-9a-f]{6}', lambda hcl: True),
    'ecl': (r'(amb|blu|brn|gry|grn|hzl|oth)', lambda ecl: True),
    'pid': (r'\d+', lambda pid: len(pid) == 9),
}

validate_fields = True  # part I / part II

valid_total = 0
passport_entries = data.split('\n\n')
for entry in passport_entries:
    passport_data = {e.split(':')[0]: e.split(':')[1] for e in entry.split()}

    has_all_requisite_fields = all(field in passport_data.keys() for field in fields)

    if has_all_requisite_fields and validate_fields:
        if all(re.match(regex, passport_data[field]) and func(passport_data[field]) for field, (regex, func) in validation_rules.items()):
            valid_total += 1
    elif has_all_requisite_fields:
        valid_total += 1

print(valid_total)

