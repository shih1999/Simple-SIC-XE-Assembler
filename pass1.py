import json
import OPTAB

# open intermediate file for pass 1 to write
pass1_output = open("intermediate_file.txt" , "w")
# open source file for assembler to read
source_file = input("Enter source file name :")
#source_file = "source.txt"

LOCCTR = 0
LAST_LOC = 0
SYM_TABLE = {}
line_count = -1

# write intermediate file in pass 1
def write_intermediate(loc, label, instruction, target):
    # add loc
    if (loc==""):
        write_line = '\t'
    else:
        write_line = hex(loc)[2:].zfill(4)              # hex : 0x__
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
    # add target
    if (target==""):
        write_line += '\n'
    else:
        write_line += '\t'
        write_line += target
        write_line += '\n'
    pass1_output.write(write_line)

def process_line(loc, label, instruction, target, add):
    global LOCCTR
    global LAST_LOC
    write_intermediate(loc, label, instruction, target)
    if (label != ""):
        SYM_TABLE[label] = LOCCTR
        LAST_LOC = LOCCTR
    LOCCTR += int(add)

def print_SYMTAB():
    print("|| SYMTAB ||\n")
    for key, value in SYM_TABLE.items():
        print("{: <15} {: <0}".format(key, value))
    print("\n")

def print_intermediate():
    print("|| Intermediate File ||\n")
    fd = open("intermediate_file.txt" , "r")
    print(fd.read())
    print("\n")

def print_pass1():
    print("PASS 1 finished.\n")
    print_SYMTAB()
    print_intermediate()

## main program ##

with open(source_file) as source_input:
    for line in source_input:
        line_count += 1

        line_len = 0
        line_label = ""
        line_instruction = ""
        line_target = ""
        
        new_line = line.split()
        line_len = len(new_line)
        flag_pass = 1
        
        if (line_len == 0):                         # empty line
            pass
        elif (line[0] == '.') :                     # comments only
            pass
        elif (line_len == 1):                       # lable or intruction
            flag_pass = 0
            if (line[0]=='\t'):                     # instruction
                line_instruction = new_line[0]
            else:                                   # label
                line_label = new_line[0]
        elif (line_len == 2):                       # intruction, target
            flag_pass = 0
            line_instruction = new_line[0]
            line_target = new_line[1]
        elif (line_len == 3):                       # lable, intruction, target
            flag_pass = 0
            line_label = new_line[0]
            line_instruction = new_line[1]
            line_target = new_line[2]
        else :
            pass
        
        #print(line_len, 'a:', line_label, 'b:', line_instruction, 'c:', line_target)

        if (flag_pass == 1):
            write_line = '\t'+line
            pass1_output.write(write_line)
        elif(line_len == 1 and line_label != ""):   # label only
            write_line = hex(LOCCTR)[2:].zfill(4)+'\t'+line_label+'\n'
            SYM_TABLE[line_label] = LOCCTR
            pass1_output.write(write_line)
        else:
            if (line_instruction[0] == "+"):
                process_line(LOCCTR, line_label, line_instruction, line_target, 4)
            elif (line_instruction == "START"):
                LOCCTR = int(line_target)
                process_line(LOCCTR, line_label, line_instruction, line_target, 0)
            elif (line_instruction == "BASE"):
                process_line("", line_label, line_instruction, line_target, 0)
            elif (line_instruction == "BYTE"):
                if (line_target[0]=='C'):
                    process_line(LOCCTR, line_label, line_instruction, line_target, len(line_target)-3)
                elif (line_target[0]=='X'):
                    process_line(LOCCTR, line_label, line_instruction, line_target, 1)
            elif (line_instruction == "WORD"):
                process_line(LOCCTR, line_label, line_instruction, line_target, 3)
            elif (line_instruction == "RESB"):
                process_line(LOCCTR, line_label, line_instruction, line_target, 1*int(line_target))
            elif (line_instruction == "RESW"):
                process_line(LOCCTR, line_label, line_instruction, line_target, 3*int(line_target))
            elif(line_instruction == "END"):
                process_line("", line_label, line_instruction, line_target, 0)
                SYM_TABLE["END"] = LAST_LOC
            else:
                process_line(LOCCTR, line_label, line_instruction, line_target, OPTAB.OP_TABLE[line_instruction][1])
pass1_output.close()
# save SYMTAB into a json file
json.dump(SYM_TABLE, open("SYMTAB.json", 'w'))

print_pass1()





            




