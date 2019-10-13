symbolTable   = {} # Hash table to implement symbol table
literalTable  = {} # dict to implement literals
macrosTable   = {} # to keep track of macros
opcodeTable   = [] # to keep track of opcode instructions
lc = 0 # Location Counter

# Proposal:
# We should add literals like "=5"
# This means we need to provide absolute value of 5 here

# We can define variables in a separate section
# .WORD ( initiates that section )
# DW <Variable_Name> <Variable_Value> 

# assemblyCode : [Opcode, instructionSize, noOfArguments, opcodeID]
opcodeList = {
    "CLA": ["0000", 1, 0, 1], # Clear Accumulator
    "LAC": ["0001", 1, 1, 2], # Load into AC from Address
    "SAC": ["0010", 1, 1, 3], # Store AC into address
    "ADD": ["0011", 1, 1, 4], # AC <- AC + M[x]
    "SUB": ["0100", 1, 1, 5], # AC <- AC - M[x]
    "BRZ": ["0101", 1, 1, 6], # Branch to address if AC == 0
    "BRN": ["0110", 1, 1, 7], # Branch to address if AC < 0 
    "BRP": ["0111", 1, 1, 8], # Branch to address if AC > 0
    "INP": ["1000", 1, 1, 9], # Take Input from terminal into address
    "DSP": ["1001", 1, 1, 10], # Display value in address
    "MUL": ["1010", 1, 1, 11], # AC <- AC * M[x]
    "DIV": ["1011", 1, 1, 12], # AC / M[x] -> R1 and AC % M[x] -> R2
    "STP": ["1100", 1, 0, 13], # Stop Execution
}

initialOffset = 0
hasStart = False
hasError = False

def comment(line):
    # Checks if the line is a comment or not
    if (line != "\n" and line.strip()[0] == "#"):
        return True
    return False

def checkSymbol(line):
    # Checks if the line is a symbol, this is done by checking if a ":" occurs in the line
    if (line == "\n"):
        return False
    couldBeSymbol = line.strip().split(' ')[0]
    if (couldBeSymbol[-1] == ':'):
        return couldBeSymbol
    else:
        return False

def addNewSymbol(symbol, lc):
    # This adds new symbol to the symbol table
    # The next 3 commands just remove ":" from symbol name
    symbol=symbol[::-1]
    symbol=symbol[1:]
    symbol=symbol[::-1]
    # print(symbol)
    if (symbol in symbolTable):
        # THis will throw error in future
        print("Error: Duplicate Symbol %s" % symbol)
    symbolTable[symbol] = int(lc)

def checkLiteral(line):
    #Checks if the line is a literal, this is done by checking if a "=" occurs in the line
    if(line =="\n"):
        return False
    couldBeLiteral = line.strip().split(' ')[0]
    if(couldBeLiteral[0]=='='):
        return couldBeLiteral
    return False

def addLiteral(literal, value):
    # Need to implement add literal

    return True

def getOpcode(parts):
    global hasStart
    global initialOffset
    i = 1
    if (len(parts) <= 0):
        return False
    if (parts[0][-1] != ':'):
        i = 0
    try:
        #print(parts)
        if (parts[0] == 'START' and len(parts) == 2):   
            if (hasStart):
                print("Can't have 2 START statements")
            else:
                hasStart = True
                initialOffset = int(parts[1])
                return False
        x = opcodeList[parts[i]]
        return x
    except:
        if (parts[0] != 'START'):
            print("%s is not a valid opcode!" % parts[i])
        return False

def isPseudoOpcode(parts):
    # Will be used if we add any pseudo literals to our language -> most prob wont be used
    return False

def handleMacros():
    # This will be tricky
    return False

def removeRedundantLiterals():
    # Go through the literal table and remove extra entries
    return False

def getType(parts):
    return 1

def decimalToBinary(dec):
    return "{0:012b}".format(int(dec))

def getVariableAddr(var):
    return var

def generateOutput(opcode, parts):
    global hasError

    if (opcode == False):
        return '\n'
    #print(parts)
    startPoint = 0
    if (parts[0][-1] == ':'):
        startPoint = 1
    if (opcode == '0000'):
        return opcode + '000000000000' + '\n'
    #elif (opcode == '0001' or opcode == '0010' or opcode == '0011' or opcode == '0100'):
    elif (opcode != '1100'):
        addr = '000000000000\n'
        if (parts[1].isdigit()):
            addr = decimalToBinary(str(parts[1]))
        else:
            try:
                addr = decimalToBinary(str(symbolTable[getVariableAddr(parts[1])] + initialOffset))
            except:
                print("Symbol %s not found in the symbol table!" % getVariableAddr(parts[1]))
                hasError = True
                return
        return opcode + addr + '\n'
    else:
        return '\n'

def passOne():
    with open('input.assembly', 'r') as reader:
        #line = reader.readline()
        lc = 0
        for line in reader:
            #print(line, end='')
            parts = line.strip().split()
            #print(parts)
            length = 0
            if (not comment(line)):
                symbol = checkSymbol(line)
                if (symbol):
                    addNewSymbol(symbol, lc)
                literal = checkLiteral(line)
                if (literal):
                    addLiteral(literal)
                opcode = getOpcode(parts)
                # type = search_opcode_table(opcode) -> given in tannenbaum don't know if we need it
                if (opcode == False):
                    pseudoOpcode = isPseudoOpcode(parts)
                    #lc += instructionSize
                    continue
                else:
                    assemblyCode = 0
                    if (symbol):
                        assemblyCode = 1
                    instructionSize = opcodeList[parts[assemblyCode]][1]
                if (opcode[0] == "1100"):
                    # The end of the file
                    removeRedundantLiterals()
                #print(opcode)
                if (opcodeList[parts[assemblyCode]][2] == 1):
                    #print(opcode)
                    opcodeTable.append([parts[assemblyCode], opcode[0], lc, parts[assemblyCode+1], 1]) # Keep 2 because of no. of bytes being 16
                else:
                    opcodeTable.append([parts[assemblyCode],opcode[0], lc, -1, 2]) # -1 signifies does not exist
            lc += instructionSize
            #line = reader.readline()

def passTwo():
    arr = []
    #with open('input.assembly', 'r') as reader:
    for line in opcodeTable:
        lc = 0
        #for line in reader:
        #parts = line.strip().split()
        parts = [line[1], str(line[3])]
        #typeCommand = getType(parts)
        typeCommand = line[2]
        #opcode = getOpcode(parts)
        opcode = line[1]
        code = "\n"
        if (typeCommand != 0):
            #print(opcode, parts)
            code = generateOutput(opcode, parts)
        #print(code)
        arr.append(code)
        lc += 1
    return arr

passOne()
#for x in opcodeTable:
#    print(x)
output = passTwo()

if (not hasError):
    for o in output:
        print(o, end='')

print("\nOpcode Table:")
for oT in opcodeTable:
    print(oT)

print("\nSymbol Table:")
print(symbolTable)
