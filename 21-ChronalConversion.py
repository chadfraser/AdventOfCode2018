def parse_opcode_data_list(opcode_data_list):
    instruction_pointer = int(opcode_data_list[0].strip()[-1])
    opcode_instructions = []
    for line in opcode_data_list[1:]:
        opcode, a, b, c = line.strip().split()
        temp_list = [opcode, int(a), int(b), int(c)]
        opcode_instructions.append(temp_list)
    return instruction_pointer, opcode_instructions


def run_opcodes(instruction_pointer, opcode_instructions, registers, seen_opcodes=None):
    seen_opcodes = seen_opcodes or set()
    opcode_dict = {"addr": (lambda r, a, b: r[a] + r[b]),
                   "addi": (lambda r, a, b: r[a] + b),
                   "mulr": (lambda r, a, b: r[a] * r[b]),
                   "muli": (lambda r, a, b: r[a] * b),
                   "banr": (lambda r, a, b: r[a] & r[b]),
                   "bani": (lambda r, a, b: r[a] & b),
                   "borr": (lambda r, a, b: r[a] | r[b]),
                   "bori": (lambda r, a, b: r[a] | b),
                   "setr": (lambda r, a, b: r[a]),
                   "seti": (lambda r, a, b: a),
                   "gtir": (lambda r, a, b: int(a > r[b])),
                   "gtri": (lambda r, a, b: int(r[a] > b)),
                   "gtrr": (lambda r, a, b: int(r[a] > r[b])),
                   "eqir": (lambda r, a, b: int(a == r[b])),
                   "eqri": (lambda r, a, b: int(r[a] == b)),
                   "eqrr": (lambda r, a, b: int(r[a] == r[b]))}

    while True:
        try:
            current_instruction_index = registers[instruction_pointer]
            current_instruction = opcode_instructions[current_instruction_index]
            instruction, a, b, c = current_instruction
            registers[c] = opcode_dict[instruction](registers, a, b)
            registers[instruction_pointer] += 1
            if registers[instruction_pointer] < 0 or registers[instruction_pointer] >= len(opcode_instructions):
                break
            # print(registers)
        except IndexError:
            break


def main():
    with open("21-ChronalConversion-Input.txt") as input_file:
        opcode_data = input_file.readlines()
    instruction_pointer, opcode_instructions = parse_opcode_data_list(opcode_data)

    register = [0, 0, 0, 0, 0, 0]
    run_opcodes(instruction_pointer, opcode_instructions, register)
    print(register)


if __name__ == "__main__":
    main()
