import OPTAB as op
import json

SYM_TABLE = {}
SYM_TABLE = json.load(open("SYMTAB.json"))

PRO_NAME = ""
BASE = 0

start_loc = 0
code_count = 0
T_record = {}
record_len = 0
written = 0

pass1_output = open("intermediate_file.txt", "r")
pass2_output = open("result_file.txt", "w")
assembler_output = open("object_code.txt", "w")

def twosComplement (value, bitLength) :
    return bin(value & (2**bitLength - 1))

def get_op(instruction):
    op_code = op.OP_TABLE[instruction][0]
    op_code = (bin(op_code)[2:]).zfill(8)[:6]
    return op_code

# format 3 obcode
def get_result_1(op, flag, disp):
    result = op + flag + disp
    result = hex(int(result,2))
    result = result[2:].zfill(6)
    return result
# format 4 obcode
def get_result_2(op, flag, add):
    result = op + flag + add
    result = hex(int(result,2))
    result = result[2:].zfill(8)
    return result

def get_disp (ta, pc):
    flag_base = 0
    disp = ta-pc
    if (disp > 2047 or disp < -2048):
        disp = ta - BASE
        flag_base = 1        
    return disp, flag_base

def write_file (loc, label, instruction, target, ob):
    write_line = ""
    # add loc
    if (loc==""):
        write_line += '\t'
    else:
        write_line += loc
        write_line += '\t'
    # add label
    if (label==""):
        write_line += '\t'
    else:
        write_line += label
        write_line += '\t'
    # add instruction
    if (instruction==""):
        write_line += '\t'
    else:
        write_line += instruction
        write_line += '\t'
    # add target
    if (target==""):
        write_line += '\t'
    else:
        write_line += target
    # add ob
    if (ob == ""):
        write_line += '\n'
    else:
        write_line += '\t'
        write_line += ob
        write_line += '\n'
    pass2_output.write(write_line)
    
def write_recode ( T_rec, count, start, len):
    written = 1
    assembler_output.write("T")
    assembler_output.write(hex(start)[2:].zfill(6))
    assembler_output.write(hex(int(len))[2:].zfill(2))
    for i in range(1, count+1):
        assembler_output.write(T_rec[i])
    assembler_output.write("\n")
    
def print_result():
    print("|| Result File ||\n")
    fd = open("result_file.txt", "r")
    print(fd.read())
    print("\n")

def print_obcode():
    print("|| Object Program ||\n")
    fd = open("object_code.txt", "r")
    print(fd.read())
    print("\n")

def print_pass2():
    print("PASS 2 finished.\n")
    print_result()
    print_obcode()
    
previous_loc = 0

for line in pass1_output:
    line_len = 0
    line_loc = ""
    line_label = ""
    line_instruction = ""
    line_target = ""
    line_result = ""
    ob_code = ""
    result_flag = ""
    flag_print = 1
        
    new_line = line.split()
    line_len = len(new_line)
    flag_pass = 1
    #print(new_line)
    test_line = line.split("\t")
    #print(test_line)

    if (line_len == 0):                         # empty line
        pass
    elif (test_line[1] == '.') :                # comments only
        pass
    elif (line_len == 2):                       # lable or intruction or label
        flag_pass = 0
        if (test_line[0]==""):                  # intruction, target
            line_instruction = new_line[0]
            line_target = new_line[1]
        elif (test_line[1]==""):                # loc, instruction
            line_loc = new_line[0]
            line_instruction = new_line[1]
        else:                                   # loc, label
            flag_pass = 1
            line_loc = new_line[0]
            line_label = new_line[1]
    elif (line_len == 3):                       # loc, intruction, target
        flag_pass = 0
        line_loc = new_line[0]
        line_instruction = new_line[1]
        line_target = new_line[2]
    elif (line_len == 4):                       # loc, lable, intruction, target
        flag_pass = 0
        line_loc = new_line[0]
        line_label = new_line[1]
        line_instruction = new_line[2]
        line_target = new_line[3]
    else :
        pass

    if (flag_pass == 1):
        pass2_output.write(line)
    else :
        #print(line_instruction)
        if (line_instruction == "START"):
            PRO_NAME = line_label
            pass2_output.write(line)
            assembler_output.write("H")
            assembler_output.write(PRO_NAME)
            assembler_output.write("\t")
            assembler_output.write(hex(SYM_TABLE[PRO_NAME])[2:].zfill(6))
            assembler_output.write(hex(SYM_TABLE["END"]-SYM_TABLE[PRO_NAME]+1)[2:].zfill(6))
            assembler_output.write("\n")
            flag_print = 0
        elif (line_instruction == "END"):
            pass2_output.write(line)
            flag_print = 0
        elif (line_instruction == "RESB" or line_instruction == "RESW"):
            pass2_output.write(line)
            flag_print = 0
        elif (line_instruction == "BASE"):
            BASE = SYM_TABLE[line_target]
            flag_print = 0
        elif(line_instruction == "BYTE"):
            temp = line_target.split('\'')
            if (temp[0] == 'X'):
                ob_code = temp[1].upper()
                write_file (line_loc, line_label, line_instruction, line_target, ob_code)
            elif (temp[0] == 'C'):
                ob_code = (hex(ord(temp[1][0]))[2:] + hex(ord(temp[1][1]))[2:] + hex(ord(temp[1][2]))[2:]).upper()
                write_file (line_loc, line_label, line_instruction, line_target, ob_code)
        elif (line_instruction == "RSUB"):
            result_op = get_op(line_instruction)
            result_flag = "110000"
            ob_code = get_result_1(result_op, result_flag, bin(0)[2:].zfill(12)).upper()
            write_file (line_loc, line_label, line_instruction, line_target, ob_code)
        elif (line_instruction == "LDCH" or line_instruction == "STCH"):
            result_op = get_op(line_instruction)
            result_flag = "111100"
            result_disp = bin(SYM_TABLE[line_target.split(',')[0]]-BASE)[2:].zfill(12)
            ob_code = get_result_1(result_op, result_flag, result_disp).upper()
            write_file (line_loc, line_label, line_instruction, line_target, ob_code)
        elif (line_instruction == "COMPR"):
            result_op = hex(op.OP_TABLE[line_instruction][0])[2:]
            ob_code = (result_op + op.REG_TABLE[line_target.split(',')[0]] + op.REG_TABLE[line_target.split(',')[1]]).upper()
            write_file (line_loc, line_label, line_instruction, line_target, ob_code)
        elif (line_instruction == "CLEAR" or line_instruction == "TIXR"):
            result_op = hex(op.OP_TABLE[line_instruction][0])[2:]
            ob_code = (result_op + op.REG_TABLE[line_target.split(',')[0]] + "0").upper()
            write_file (line_loc, line_label, line_instruction, line_target, ob_code)
        else :
            n = "0"
            i = "0"
            x = "0"
            b = "0"
            p = "0"
            e = "0"
            flag_extend = 0
            flag_immediate = 0
            flag_indirect = 0
            if (line_instruction[0] == "+"):
                flag_extend = 1
                e = "1"
                line_instruction = line_instruction[1:]
                result_op = get_op(line_instruction)
            else:
                result_op = get_op(line_instruction)
            # immediate addressing
            if (line_target[0] == '#'):
                temp_symbol = line_target[1:]
                flag_immediate = 1
                i = "1"
            # indirect addressing
            elif (line_target[0] == '@'):
                temp_symbol = line_target[1:]
                flag_indirect = 1
                n = "1"
            else: 
                i = "1"
                n = "1"
            if (line_target[0] == '#' and (line_target[1:].isnumeric() == True)):
                result_flag =  n+i+x+b+p+e
                if (flag_extend == 1):
                    result_disp = (bin(int(temp_symbol))[2:]).zfill(20)
                    ob_code = get_result_2(result_op, result_flag, result_disp).upper()
                    write_file (line_loc, line_label, line_instruction, line_target, ob_code)
                else:
                    result_disp = (bin(int(temp_symbol))[2:]).zfill(12)
                    ob_code = get_result_1(result_op, result_flag, result_disp).upper()
                    write_file (line_loc, line_label, line_instruction, line_target, ob_code)
            else:
                if (line_target[0] == '#' or line_target[0] == '@'):
                    symbol = SYM_TABLE[temp_symbol]
                else:
                    symbol = SYM_TABLE[line_target]
                # format 4
                if (flag_extend == 1):
                    disp = symbol
                    if (int(disp) < 0):
                        result_disp = twosComplement (int(disp), 20)[2:]
                    else:
                        result_disp = (bin(int(disp))[2:]).zfill(20)
                    result_flag =  n+i+x+b+p+e
                    ob_code = get_result_2(result_op, result_flag, result_disp).upper()
                    write_file (line_loc, line_label, line_instruction, line_target, ob_code)
                # format 3
                else:
                    disp, flag_base = get_disp(symbol, int(line_loc, 16)+3)
                    if (flag_base == 0):
                        p = "1"
                    else:
                        b = "1"
                    result_flag =  n+i+x+b+p+e
                    if (int(disp) < 0):
                        result_disp = twosComplement (int(disp), 12)[2:]
                    else:
                        result_disp = (bin(int(disp))[2:]).zfill(12)
                    ob_code = get_result_1(result_op, result_flag, result_disp).upper()
                    write_file (line_loc, line_label, line_instruction, line_target, ob_code)
    # write Object Program
    if (flag_print == 0):
        pass
    else:
        #print(code_count, line_instruction, T_record)
        if ((int(line_loc, 16) - previous_loc > 4) and code_count != 0):
            write_recode (T_record, code_count, start_loc, record_len)
            start_loc = 0
            code_count = 0
            T_record = {}
            record_len = 0
            written = 0
            code_count += 1
            start_loc = int(line_loc, 16)
            T_record[code_count] = ob_code
            record_len += len(ob_code)/2
        else :
            code_count += 1
            record_len += len(ob_code)/2
            T_record[code_count] = ob_code
            if (code_count == 1):
                start_loc = int(line_loc, 16)
            if (code_count == 9):
                write_recode (T_record, code_count, start_loc, record_len)
                start_loc = 0
                code_count = 0
                T_record = {}
                record_len = 0
                written = 0
            else:
                pass
        previous_loc = int(line_loc, 16)
        
if (written == 0):
    write_recode ( T_record, code_count, start_loc, record_len)
assembler_output.write("E")
assembler_output.write(hex(SYM_TABLE[PRO_NAME])[2:].zfill(6))
                 
pass1_output.close()
pass2_output.close()
assembler_output.close()

print_pass2()