symbolTable   = {} # Hash table to implement symbol table
literalTable = {} # dict to implement literals
macrosTable   = {} # to keep track of macros
lc = 0 # Location Counter

# assemblyCode : [Opcode, instructionSize]
opcodeTable = {
    "CLA": ["0000", 1], # Clear Accumulator
    "LAC": ["0001", 1], # Load into AC from Address
    "SAC": ["0010", 1], # Store AC into address
    "ADD": ["0011", 1], # AC <- AC + M[x]
    "SUB": ["0100", 1], # AC <- AC - M[x]
    "BRZ": ["0101", 1], # Branch to address if AC == 0
    "BRN": ["0110", 1], # Branch to address if AC < 0 
    "BRP": ["0111", 1], # Branch to address if AC > 0
    "INP": ["1000", 1], # Take Input from terminal into address
    "DSP": ["1001", 1], # Display value in address
    "MUL": ["1010", 1], # AC <- AC * M[x]
    "DIV": ["1011", 1], # AC / M[x] -> R1 and AC % M[x] -> R2
    "STP": ["1100", 1], # Stop Execution
}


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
    if (symbol in symbolTable):
        # THis will throw error in future
        print("Duplicate Symbol")
    symbolTable[symbol] = lc

def checkLiteral(line):
    # Need to be implemented
    return False

def addLiteral(literal):
    # Need to implement add literal
    return True

def getOpcode(parts):
    i = 1
    if (len(parts) <= 0):
        return False
    if (parts[0][-1] != ':'):
        i = 0
    try:
        x = opcodeTable[parts[i]]
        return x
    except:
        print("%s is not a valid opcode!", parts[i])
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

with open('input.assembly', 'r') as reader:
    line = reader.readline()
    while line != '':
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
                break
            else:
                assemblyCode = 0
                if (symbol):
                    assemblyCode = 1
                instructionSize = opcodeTable[parts[assemblyCode]][1]
                lc += instructionSize
            if (opcode[0] == "1100"):
                # The end of the file
                removeRedundantLiterals()
            # print(opcode)
        line = reader.readline()

print(symbolTable)