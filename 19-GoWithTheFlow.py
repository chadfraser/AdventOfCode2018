# def addr(registers, a, b, c):
#     registers[c] = registers[a] + registers[b]
#     return registers
#
#
# def addi(registers, a, b, c):
#     registers[c] = registers[a] + b
#     return registers
#
#
# def mulr(registers, a, b, c):
#     registers[c] = registers[a] * registers[b]
#     return registers
#
#
# def muli(registers, a, b, c):
#     registers[c] = registers[a] * b
#     return registers
#
#
# def banr(registers, a, b, c):
#     registers[c] = registers[a] & registers[b]
#     return registers
#
#
# def bani(registers, a, b, c):
#     registers[c] = registers[a] & b
#     return registers
#
#
# def borr(registers, a, b, c):
#     registers[c] = registers[a] | registers[b]
#     return registers
#
#
# def bori(registers, a, b, c):
#     registers[c] = registers[a] | b
#     return registers
#
#
# def setr(registers, a, b, c):
#     registers[c] = registers[a]
#     return registers
#
#
# def seti(registers, a, b, c):
#     registers[c] = a
#     return registers
#
#
# def gtir(registers, a, b, c):
#     registers[c] = bool(a > registers[b])
#     return registers
#
#
# def gtri(registers, a, b, c):
#     registers[c] = bool(registers[a] > b)
#     return registers
#
#
# def gtrr(registers, a, b, c):
#     registers[c] = bool(registers[a] > registers[b])
#     return registers
#
#
# def eqir(registers, a, b, c):
#     registers[c] = bool(a == registers[b])
#     return registers
#
#
# def eqri(registers, a, b, c):
#     registers[c] = bool(registers[a] == b)
#     return registers
#
#
# def eqrr(registers, a, b, c):
#     registers[c] = bool(registers[a] == registers[b])
#     return registers


def parse_opcode_data_list(opcode_data_list):
    instruction_pointer = int(opcode_data_list[0].strip()[-1])
    opcode_instructions = []
    for line in opcode_data_list[1:]:
        opcode, a, b, c = line.strip().split()
        temp_list = [opcode, int(a), int(b), int(c)]
        opcode_instructions.append(temp_list)
    return instruction_pointer, opcode_instructions


def run_opcodes(instruction_pointer, opcode_instructions, registers):
    # opcode_dict = {"addi": (lambda r, a, b: r[a] + r[b]),
    #                "addr": addr, "muli": muli, "mulr": mulr, "bani": bani, "banr": banr, "bori": bori,
    #                "borr": borr, "seti": seti, "setr": setr, "gtir": gtir, "gtri": gtri, "gtrr": gtrr, "eqir": eqir,
    #                "eqri": eqri, "eqrr": eqrr}
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
        except IndexError:
            break
        # 974


def main():
    with open("19-GoWithTheFlow-Input.txt") as input_file:
        opcode_data_list = input_file.readlines()
    instruction_pointer, opcode_instructions = parse_opcode_data_list(opcode_data_list)

    register = [0, 0, 0, 0, 0, 0]
    run_opcodes(instruction_pointer, opcode_instructions, register)
    print(register)

    register_b = [1, 0, 0, 0, 0, 0]
    # run_opcodes(instruction_pointer, opcode_instructions, register_b)
    print(register_b)


if __name__ == "__main__":
    main()

def main():
    with open("19-GoWithTheFlow-Input.txt") as input_file:
        opcode_data_list = input_file.readlines()
    instruction_pointer, opcode_instructions = parse_opcode_data_list(opcode_data_list)

    register = [0, 0, 0, 0, 0, 0]
    run_opcodes(instruction_pointer, opcode_instructions, register)
    print(register)

    register_b = [1, 0, 0, 0, 0, 0]
    # run_opcodes(instruction_pointer, opcode_instructions, register_b)
    print(register_b)


if __name__ == "__main__":
    main()
