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

# assemblyCode : [Opcode, instructionSize, noOfArguments]
opcodeList = {
    "CLA": ["0000", 2, 0], # Clear Accumulator
    "LAC": ["0001", 2, 1], # Load into AC from Address
    "SAC": ["0010", 2, 1], # Store AC into address
    "ADD": ["0011", 2, 1], # AC <- AC + M[x]
    "SUB": ["0100", 2, 1], # AC <- AC - M[x]
    "BRZ": ["0101", 2, 1], # Branch to address if AC == 0
    "BRN": ["0110", 2, 1], # Branch to address if AC < 0 
    "BRP": ["0111", 2, 1], # Branch to address if AC > 0
    "INP": ["1000", 2, 1], # Take Input from terminal into address
    "DSP": ["1001", 2, 1], # Display value in address
    "MUL": ["1010", 2, 1], # AC <- AC * M[x]
    "DIV": ["1011", 2, 1], # AC / M[x] -> R1 and AC % M[x] -> R2
    "STP": ["1100", 2, 0], # Stop Execution
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
    # This adds new symbol to the symbol table
    # The next 3 commands just remove ":" from symbol name
    symbol=symbol[::-1]
    symbol=symbol[1:]
    symbol=symbol[::-1]
    # print(symbol)
    if (symbol in symbolTable):
        # THis will throw error in future
        print("Duplicate Symbol")
    symbolTable[symbol] = lc

def checkLiteral(line):
    # Need to be implemented
    return False

def addLiteral(literal, value):
    # Need to implement add literal

    return True

def getOpcode(parts):
    i = 1
    if (len(parts) <= 0):
        return False
    if (parts[0][-1] != ':'):
        i = 0
    try:
        x = opcodeList[parts[i]]
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
            if (opcode== False):
                pseudoOpcode = isPseudoOpcode(parts)
                break
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
                opcodeTable.append([opcode[0], lc, parts[assemblyCode+1], 2]) # Keep 2 because of no. of bytes being 16
            else:
                opcodeTable.append([opcode[0], lc, -1, 2]) # -1 signifies does not exist
            lc += instructionSize


        line = reader.readline()

print(symbolTable)
for x in opcodeTable:
    print(x)