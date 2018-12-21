def check_if_other_registers_changed(original_registers, final_registers, c):
    for index, (original_value, final_value) in enumerate(zip(original_registers, final_registers)):
        if index != c and original_value != final_value:
            return False


def addr(registers, a, b, c):
    registers[c] = registers[a] + registers[b]
    return registers


def is_addr(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] + original_registers[b] == final_registers[c]


def addi(registers, a, b, c):
    registers[c] = registers[a] + b
    return registers


def is_addi(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] + b == final_registers[c]


def is_mulr(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] * original_registers[b] == final_registers[c]


def mulr(registers, a, b, c):
    registers[c] = registers[a] * registers[b]
    return registers


def is_muli(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] * b == final_registers[c]


def muli(registers, a, b, c):
    registers[c] = registers[a] * b
    return registers


def is_banr(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] & original_registers[b] == final_registers[c]


def banr(registers, a, b, c):
    registers[c] = registers[a] & registers[b]
    return registers


def is_bani(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] & b == final_registers[c]


def bani(registers, a, b, c):
    registers[c] = registers[a] & b
    return registers


def is_borr(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] | original_registers[b] == final_registers[c]


def borr(registers, a, b, c):
    registers[c] = registers[a] | registers[b]
    return registers


def is_bori(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] | b == final_registers[c]


def bori(registers, a, b, c):
    registers[c] = registers[a] | b
    return registers


def is_setr(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return original_registers[a] == final_registers[c]


def setr(registers, a, b, c):
    registers[c] = registers[a]
    return registers


def is_seti(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return a == final_registers[c]


def seti(registers, a, b, c):
    registers[c] = a
    return registers


def is_gtir(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return bool(a > original_registers[b]) == final_registers[c]


def gtir(registers, a, b, c):
    registers[c] = bool(a > registers[b])
    return registers


def is_gtri(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return bool(original_registers[a] > b) == final_registers[c]


def gtri(registers, a, b, c):
    registers[c] = bool(registers[a] > b)
    return registers


def is_gtrr(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return bool(original_registers[a] > original_registers[b]) == final_registers[c]


def gtrr(registers, a, b, c):
    registers[c] = bool(registers[a] > registers[b])
    return registers


def is_eqir(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return bool(a == original_registers[b]) == final_registers[c]


def eqir(registers, a, b, c):
    registers[c] = bool(a == registers[b])
    return registers


def is_eqri(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return bool(original_registers[a] == b) == final_registers[c]


def eqri(registers, a, b, c):
    registers[c] = bool(registers[a] == b)
    return registers


def is_eqrr(original_registers, final_registers, a, b, c):
    if check_if_other_registers_changed(original_registers, final_registers, c):
        return False
    return bool(original_registers[a] == original_registers[b]) == final_registers[c]


def eqrr(registers, a, b, c):
    registers[c] = bool(registers[a] == registers[b])
    return registers


def test_opcode(original_registers, final_registers, a, b, c):
    list_of_opcode_functions = [is_addi, is_addr, is_muli, is_mulr, is_bani, is_banr, is_bori, is_borr,
                                is_seti, is_setr, is_gtir, is_gtri, is_gtrr, is_eqir, is_eqri, is_eqrr]
    successful_tests = set()
    for opcode in list_of_opcode_functions:
        test_result = opcode(original_registers, final_registers, a, b, c)
        if test_result:
            successful_tests.add(opcode)
    return successful_tests


def run_opcode(register, instruction, opcode_key_dict):
    opcode, a, b, c = instruction
    register = opcode_key_dict[opcode](register, a, b, c)
    return register


def test_all_opcodes(opcode_data_list):
    sum_of_opcodes_of_three_or_more_instructions = 0
    for opcode_data in opcode_data_list:
        original_registers, instructions, final_registers = opcode_data
        __, a, b, c = instructions
        opcode_sum = len(test_opcode(original_registers, final_registers, a, b, c))
        if opcode_sum >= 3:
            sum_of_opcodes_of_three_or_more_instructions += 1
    return sum_of_opcodes_of_three_or_more_instructions


def determine_opcode_rules(opcode_data_list):
    opcode_rules = {}
    for opcode_data in opcode_data_list:
        original_registers, instructions, final_registers = opcode_data
        rule_value, a, b, c = instructions
        opcode_result = test_opcode(original_registers, final_registers, a, b, c)
        opcode_rules.setdefault(rule_value, opcode_result)
        opcode_rules[rule_value] = opcode_rules[rule_value].intersection(opcode_result)

    set_opcodes = {key: value for key, value in opcode_rules.items() if len(value) == 1}
    unset_opcodes = {key: value for key, value in opcode_rules.items() if len(value) != 1}
    while unset_opcodes:
        updated_set_opcodes = {key: value for key, value in set_opcodes.items()}
        updated_unset_opcodes = {}
        for opcode, set_of_functions in unset_opcodes.items():
            temp_set_of_functions = set(function_value for function_value in set_of_functions if {function_value}
                                        not in set_opcodes.values())
            if len(temp_set_of_functions) == 1:
                updated_set_opcodes[opcode] = temp_set_of_functions
            else:
                updated_unset_opcodes[opcode] = temp_set_of_functions

        set_opcodes = updated_set_opcodes
        unset_opcodes = updated_unset_opcodes
    translated_opcodes = key_opcodes(set_opcodes)
    return translated_opcodes


def key_opcodes(opcode_key_dict):
    opcode_key_translation = {is_addi: addi, is_addr: addr, is_muli: muli, is_mulr: mulr, is_bani: bani, is_banr: banr,
                              is_bori: bori, is_borr: borr, is_seti: seti, is_setr: setr, is_gtir: gtir, is_gtri: gtri,
                              is_gtrr: gtrr, is_eqir: eqir, is_eqri: eqri, is_eqrr: eqrr}
    new_opcode_key_dict = {}
    for key, set_value in opcode_key_dict.items():
        for value in set_value:
            new_opcode_key_dict[key] = opcode_key_translation[value]
    return new_opcode_key_dict


def parse_opcode_data(data_file):
    opcode_data = []
    index = 0
    while True:
        next_data_line = data_file.readline().strip()
        if next_data_line == "":
            break

        temp_data = next_data_line.split("[")[1]
        temp_data = temp_data.split(",")
        original_register = [int(value.strip().strip("]")) for value in temp_data]

        next_data_line = data_file.readline().strip()
        instructions = [int(value) for value in next_data_line.split()]

        next_data_line = data_file.readline().strip()
        temp_data = next_data_line.split("[")[1]
        temp_data = temp_data.split(",")
        final_register = [int(value.strip().strip("]")) for value in temp_data]
        new_opcode_data = [original_register, instructions, final_register]

        data_file.readline()
        opcode_data.append(new_opcode_data)
    list_of_instructions = []
    for line in data_file:
        if line.strip():
            next_data_line = line.strip()
            instructions = [int(value) for value in next_data_line.split()]
            list_of_instructions.append(instructions)
    return opcode_data, list_of_instructions


def main():
    with open("16-ChronalClassification-Input.txt") as input_file:
        list_of_opcodes, list_of_instructions = parse_opcode_data(input_file)
    total_opcode_sum = test_all_opcodes(list_of_opcodes)
    print(total_opcode_sum)

    opcode_rules = determine_opcode_rules(list_of_opcodes)

    for opcode, val in sorted(opcode_rules.items()):
        print(f"{opcode}:  {val}")
    register = [0, 0, 0, 0]
    print(list_of_instructions)
    input()
    for opcode in list_of_instructions:
        register = run_opcode(register, opcode, opcode_rules)
    #     print(register)
    print(register)


if __name__ == "__main__":
    main()
