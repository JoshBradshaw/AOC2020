import fileinput
import re
from copy import copy

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)


def part1(instructions):

    def apply_mask(value, mask):
        for bit, mask_val in enumerate(reversed(mask)):
            if mask_val == '0':
                value &= ~(1 << bit)
            elif mask_val == '1':
                value |= (1 << bit)
            else:
                pass
        return value

    mem = {}
    mask = ''
    for line in instructions:
        if 'mask' in line:
            mask = line.split(' = ')[1].strip()
        else:
            address, value = [int(n) for n in re.match(r'mem\[(\d+)\] = (\d+)', line).groups()]
            mem[address] = apply_mask(value, mask)

    return sum(mem.values())

def part2(instructions):
    def apply_mask(mem_address, mask):
        for bit, mask_val in enumerate(reversed(mask)):
            if mask_val == '1':
                mem_address |= (1 << bit)

        mem_addresses = set([mem_address])
        for bit, mask_val in enumerate(reversed(mask)):
            if mask_val == 'X':
                for ma in copy(mem_addresses):
                    mem_addresses.add(ma | (1 << bit))
                    mem_addresses.add(ma & ~(1 << bit))

        return mem_addresses

    mem = {}
    mask = ''
    for line in instructions:
        if 'mask' in line:
            mask = line.split(' = ')[1].strip()
        else:
            address, value = [int(n) for n in re.match(r'mem\[(\d+)\] = (\d+)', line).groups()]
            mem_addresses = apply_mask(address, mask)
            for address in mem_addresses:
                mem[address] = value
    return sum(mem.values())



instructions = [line for line in fileinput.input()]
print(part1(instructions))
print(part2(instructions))