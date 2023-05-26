import sys

if len(sys.argv) != 2:
    print("Invalid amount of arguments!")

ram = [0] * 255

programPointer = 0
currentFun = "main"
ramPointer = 0

contents = ""

functions = []
functions_code = []

with open(sys.argv[1]) as f:
    contents = "".join(f.readlines())


cf = "nul"
for l in contents.split("\n"):
    if l.startswith("fun"):
        cf = l.replace("fun ", "").replace(":", "")
        functions.append(cf)
        functions_code.append("")
    else:
        cfi = functions.index(cf)
        functions_code[cfi] += l


def get_code(fun):
    return functions_code[functions.index(fun)]


def is_num_conv(s):
    if s.isnumeric():
        return float(s)
    return s


programEnd = False


def interpret(lineId, fun):
    global ramPointer
    global programPointer
    global currentFun
    global programEnd
    global functions
    global functions_code

    sp = get_code(fun).split(";")
    if lineId > len(sp)-1:
        programEnd = True
        return

    line = sp[lineId].replace("\n", "").strip()

    if line == "":
        programPointer += 1
        return

    cmd = line.split("(")[0]
    argblock = line.split("(", 1)[1]
    argblock = argblock[::-1].replace(")", "", 1)[::-1]
    argblock = argblock.replace("\\,", "####\\COMMA\\####")
    args = argblock.split(",")

    for it, a in enumerate(args):
        args[it] = a.replace("####\\COMMA\\####", ",")

    if cmd == "in":
        ram[ramPointer] = input()

    elif cmd == "out":
        if len(args) > 1:
            print(ram[int(args[0])])
        else:
            print(ram[ramPointer])

    elif cmd == "pri":
        if len(args) > 1:
            print(ram[int(args[0])], end='')
        else:
            print(ram[ramPointer], end='')

    elif cmd == "pra":
        if len(args) > 1 and args[0] != '':
            s = ""
            for i in range(int(args[0]), int(args[1])):
                s += str(ram[i])
            print(s)
        else:
            s = ""
            for i in range(ramPointer, ramPointer+int(args[0])):
                print(ram[i])
                s += str(ram[i])
            print(s)

    elif cmd == "srp":  # set ram pointer
        ramPointer = args[0]

    elif cmd == "cpa":   # copies the value to other pos (absoulute)
        ram[int(args[0])] = ram[ramPointer]

    elif cmd == "cpr":   # copies the value to other pos (relative)
        ram[ramPointer+int(args[0])] = ram[ramPointer]

    elif cmd == "sad":
        ram[ramPointer] += float(args[0])

    elif cmd == "ssu":
        ram[ramPointer] -= float(args[0])

    elif cmd == "smu":
        ram[ramPointer] *= float(args[0])

    elif cmd == "ad1":
        ram[ramPointer] += ram[int(args[0])]

    elif cmd == "sb1":
        ram[ramPointer] -= ram[int(args[0])]

    elif cmd == "mu1":
        ram[ramPointer] *= ram[int(args[0])]

    elif cmd == "ad2":
        ram[ramPointer] = ram[int(args[0])] + ram[int(args[1])]

    elif cmd == "sb2":
        ram[ramPointer] = ram[int(args[0])] - ram[int(args[1])]

    elif cmd == "mu2":
        ram[ramPointer] = ram[int(args[0])] * ram[int(args[1])]

    elif cmd == "smo":  # self modulo
        ram[ramPointer] = ram[ramPointer] % float(args[0])

    elif cmd == "irp":  # increment ram pointer
        if len(args) > 0 and args[0] != '':
            ramPointer += int(args[0])
        else:
            ramPointer += 1

    elif cmd == "drp":  # decrement ram pointer
        if len(args) > 0 and args[0] != '':
            ramPointer -= args[0]
        else:
            ramPointer -= 1

    elif cmd == "sto":  # immediate stores a value into ram
        if args[0].isnumeric():
            ram[ramPointer] = float(args[0])
        else:
            ram[ramPointer] = args[0]

    elif cmd == "halt":
        sys.exit("Program halted")

    elif cmd == "jmp":
        currentFun = args[0]
        programPointer = 0
        return

    elif cmd == "bre":
        if is_num_conv(args[0]) == ram[ramPointer]:
            currentFun = args[1]
            programPointer = 0
            return

    elif cmd == "bne":
        if is_num_conv(args[0]) != ram[ramPointer]:
            currentFun = args[1]
            programPointer = 0
            return

    elif cmd == "bls":
        if is_num_conv(args[0]) < ram[ramPointer]:
            currentFun = args[1]
            programPointer = 0
            return

    elif cmd == "bgr":
        if is_num_conv(args[0]) > ram[ramPointer]:
            currentFun = args[1]
            programPointer = 0
            return

    elif cmd in functions:
        currentFun = cmd
        programPointer = 0
        return

    else:
        print("Instruction "+cmd+" not found!")
        sys.exit(-1)

    programPointer += 1

    if programPointer > len(get_code(fun).split(";"))-1:
        programEnd = True
        return


while not programEnd:
    interpret(programPointer, currentFun)