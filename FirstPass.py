symbolTable   = {} # Hash table to implement symbol table
literalTable = {} # dict to implement literals
macrosTable   = {} # to keep track of macros
lc = 0 # Location Counter

opcodeTable = {
    "CLA": "0000", # Clear Accumulator
    "LAC": "0001", # Load into AC from Address
    "SAC": "0010", # Store AC into address
    "ADD": "0011", # AC <- AC + M[x]
    "SUB": "0100", # AC <- AC - M[x]
    "BRZ": "0101", # Branch to address if AC == 0
    "BRN": "0110", # Branch to address if AC < 0 
    "BRP": "0111", # Branch to address if AC > 0
    "INP": "1000", # Take Input from terminal into address
    "DSP": "1001", # Display value in address
    "MUL": "1010", # AC <- AC * M[x]
    "DIV": "1011", # AC / M[x] -> R1 and AC % M[x] -> R2
    "STP": "1100", # Stop Execution
}

with open('input.assembly', 'r') as reader:
    line = reader.readline()
    while line != '':
        print(line, end='')
        parts = line.strip().split()
        print(parts)
        length = 0
        if (not comment(line)):
            symbol = checkSymbol(line)
            if (symbol != False):
                addNewSymbol(symbol, lc)
            literal = checkLiteral(line)
            if (literal != False):
                addLiteral(literal)
        line = reader.readline()


def comment(line):
    if (line.strip()[0] == "#"):
        return True
    return False

def checkSymbol(line):
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

def checkLiteral():
    # Need to be implemented
    return False

def addLiteral(literal):
    # Need to implement add literal
    return True

def getOpcode(parts):
    return True