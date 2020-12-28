with open('input.txt') as f:
    instructions = f.read().split('\n')

ins_ptr = 0
nop_jmp_change = 0

while ins_ptr < len(instructions):
    visited = set()
    acc = 0
    nop_jmp_index = 0
    ins_ptr = 0
    while ins_ptr not in visited:
        if ins_ptr == len(instructions):
            print("finished acc: ", acc)
            break

        visited.add(ins_ptr)
        instruction, value = instructions[ins_ptr].split()
        value = int(value)

        if instruction == 'nop' and nop_jmp_index == nop_jmp_change:
            instruction = 'jmp'
        if instruction == 'jmp' and nop_jmp_index == nop_jmp_change:
            instruction = 'nop'

        if instruction == 'nop':
            ins_ptr = ins_ptr + 1
            nop_jmp_index += 1
        elif instruction == 'jmp':
            ins_ptr = ins_ptr + value
            nop_jmp_index += 1
        else:
            acc += value
            ins_ptr = ins_ptr + 1

    nop_jmp_change += 1

print(acc)