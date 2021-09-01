from sys import *

tokens = []
num_stack = []
symbols = {}

def lex(filecontents):
    tok = ""
    state = 0
    string = ""
    expr = ""
    n = ""
    isexpr = 0
    varStarted = 0
    var = ""
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "PRINT" or tok == "print" or tok == "Print":
            tokens.append("PRINT")
            tok = ""
        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\n" or tok == "<EOF>":
            if expr != "" or isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM" + expr)
            elif var != "" and state == 0:
                tokens.append("VAR:" + var)
                var = ""
            tok = ""
        elif tok == "=":
            tokens.append("EQUALS")
            tok = ""
            var = ""
            varStarted = 0
        elif tok == "$" and state == 0:
            varStarted = 1
            var += tok
            tok = ""
        elif varStarted == 1:
            var += tok
            tok = ""
        elif tok == "\"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    #print(tokens)
    #return ''
    return tokens

def evalEx(expr):
    return eval(expr)

def doprint(toPrint):
    if toPrint[0:6] == "STRING":
        toPrint = toPrint[8:]
        toPrint = toPrint[:-1]
    elif toPrint[0:3] == "NUM":
        toPrint = toPrint[4:]
    elif toPrint[0:4] == "EXPR":
        toPrint = eval(toPrint[5:])
    print(toPrint)

def parse(toks):
    i = 0
    while(i < len(toks)):
        if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR":
            if toks[i+1][0:6] == "STRING":
                doprint(toks[i+1])
            elif toks[i+1][0:3] == "NUM":
                doprint(toks[i+1])
            elif toks[i+1][0:4] == "EXPR":
                doprint(toks[i+1])
        i+=2
    if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING":
        print(toks)[i+2]
        i+=3

def run():
    data = data = open(argv[1], "r").read()
    data += "<EOF>"
    toks = lex(data)
    parse(toks)

run()