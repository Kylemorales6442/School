#! C:\Program Files\Python26\pythonw
import sys, string

norw = 30      #number of reserved words
txmax = 100   #length of identifier table
nmax = 14      #max number of digits in number
al = 10          #length of identifiers
CXMAX = 500 #maximum allowed lines of assembly code
STACKSIZE = 500
a = []
chars = []
rword = []
table = []         #symbol table
code = []         #code array
stack = [0] * STACKSIZE     #interpreter stack
global infile, outfile, ch, sym, id, num, linlen, kk, line, errorFlag, linelen, codeIndx, prevIndx, codeIndx0
#-------------values to put in the symbol table------------------------------------------------------------
class tableValue():                          
    def __init__(self, name, kind, level, adr, value, params):
        self.name = name
        self.kind = kind
        self.adr = adr
        self.value = value
        self.level = level
        self.params = params
#----------commands to put in the array of assembly code-----------------------------------------------
class Cmd():                            
    def __init__(self, line, cmd, statLinks, value):
        self.line = line
        self.cmd = cmd
        self.statLinks = statLinks
        self.value = value
#-------------function to generate assembly commands--------------------------------------------------
def gen(cmd, statLinks, value):            
    global codeIndx, CXMAX
    if codeIndx > CXMAX:
        print >>outfile, "Error, Program is too long"
        exit(0)
    x = Cmd(codeIndx, cmd, statLinks, value)
    code.append(x)
    codeIndx += 1
#--------------function to change jump commands---------------------------------------
def fixJmp(cx, jmpTo):
    code[cx].value = jmpTo
#--------------Function to print p-Code for a given block-----------------------------
def printCode():
    global codeIndx, codeIndx0
    print>>outfile
    for i  in range(codeIndx0, codeIndx):
        print >>outfile, code[i].line, code[i].cmd, code[i].statLinks, code[i].value
    prevIndx = codeIndx
#-------------Function to find a new base----------------------------------------------
def Base(statLinks, base):
    b1 = base
    while(statLinks > 0):
        b1 = stack[b1]
        statLinks -= 1
    return b1
#-------------P-Code Interpreter-------------------------------------------------------
def Interpret():
    print >>outfile, "Start PL/0"
    top = 0
    base = 1
    pos = 0
    stack[1] = 0
    stack[2] = 0
    stack[3] = 0
    while True:
        instr = code[pos]
        pos += 1
        #       LIT COMMAND
        if instr.cmd == "LIT":    
            top += 1
            stack[top] = int(instr.value)

        #       OPR COMMAND
        elif instr.cmd == "OPR":
            if instr.value == 0:         #end
                top = base - 1
                base = stack[top+2]
                pos = stack[top + 3]
            elif instr.value == 1:         #unary minus
                stack[top] = -stack[top]
            elif instr.value == 2:         #addition
                top -= 1
                stack[top] = stack[top] + stack[top+1]
            elif instr.value == 3:         #subtraction
                top -= 1
                stack[top] = stack[top] - stack[top+1]
            elif instr.value == 4:         #multiplication
                top -= 1
                stack[top] = stack[top] * stack[top+1]
            elif instr.value == 5:         #integer division
                top -= 1
                stack[top] = stack[top] / stack[top+1]
            elif instr.value == 6:         #logical odd function
                if stack[top] % 2 == 0:
                    stack[top] = 1
                else:
                    stack[top] = 0
            # case 7 n/a, used to debuge programs
            elif instr.value == 8:        #test for equality if stack[top-1] = stack[top], replace pair with true, otherwise false
                top -= 1
                if stack[top] == stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 9:         #test for inequality
                top -= 1
                if stack[top] != stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 10:         #test for < (if stack[top-1] < stack[t])
                top -= 1
                if stack[top] < stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 11:        #test for >=
                top -= 1
                if stack[top] >= stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 12:        #test for >
                top -= 1
                if stack[top] > stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 13:        #test for <=
                top -= 1
                if stack[top] <= stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 14:        #write/print stack[top]  
                print >>outfile, stack[top],
                top -= 1
            elif instr.value == 15:        #write/print a newline
                print

        #      LOD COMMAND
        elif instr.cmd == "LOD":
            top += 1
            stack[top] = stack[Base(instr.statLinks, base) + instr.value]

        #    STO COMMAND
        elif instr.cmd == "STO":
            stack[Base(instr.statLinks, base) + instr.value] = stack[top]
            top -= 1

        #    CAL COMMAND
        elif instr.cmd == "CAL": 
            stack[top+1] = Base(instr.statLinks, base)
            stack[top+2] = base
            stack[top+3] = pos
            base = top + 1
            pos = instr.value

        #    INT COMMAND
        elif instr.cmd == "INT":
            top = top + instr.value

        #    JMP COMMAND
        elif instr.cmd == "JMP":
            pos = instr.value

        #    JPC COMMAND
        elif instr.cmd == "JPC":
            if stack[top] == instr.statLinks:
                pos = instr.value
            top -= 1

        # Begin new code
        #    CTS COMMAND
        elif instr.cmd == "CTS":
            top += 1
            stack[top] = stack[top-1]
        # End new code

        # Begin new code (compiler 4)
        elif instr.cmd == "STI":
            stack[stack[base(table[i].level) + table[i].adr]] = stack[top]
            top -= top

        elif instr.cmd == "LDI":
            top += top
            stack[top] = stack[stack[base(table[i].level) + table[i].adr]]

        elif instr.cmd == "LDA":
            top += top
            stack[top] = base(table[i].level) + table[i].adr
        # End new code

        if pos == 0:
            break
            
    print "End PL/0"
#--------------Error Messages----------------------------------------------------------
def error(num):
    global errorFlag;
    errorFlag = 1
    print
    if num == 1: 
        print >>outfile, "Use = instead of :="
    elif num ==2: 
        print >>outfile, "= must be followed by a number."
    elif num ==3: 
        print >>outfile, "Identifier must be followed by ="
    elif num ==4: 
        print >>outfile, "Const, Var, Procedure must be followed by an identifier."
    elif num ==5: 
        print >>outfile, "Semicolon or comman missing"
    elif num == 6: 
        print >>outfile, "Incorrect symbol after procedure declaration."
    elif num == 7:  
        print >>outfile, "Statement expected."
    elif num == 8:
        print >>outfile, "Incorrect symbol after statment part in block."
    elif num == 9:
        print >>outfile, "Period expected."
    elif num == 10: 
        print >>outfile, "Semicolon between statements is missing."
    elif num == 11:  
        print >>outfile, "Undeclard identifier"
    elif num == 12:
        print >>outfile, "Assignment to a constant or procedure is not allowed."
    elif num == 13:
        print >>outfile, "Assignment operator := expected."
    elif num == 14: 
        print >>outfile, "call must be followed by an identifier"
    elif num == 15:  
        print >>outfile, "Call of a constant or a variable is meaningless."
    elif num == 16:
        print >>outfile, "Then expected"
    elif num == 17:
        print >>outfile, "Semicolon or end expected. "
    elif num == 18: 
        print >>outfile, "DO expected"
    elif num == 19:  
        print >>outfile, "Incorrect symbol following statement"
    elif num == 20:
        print >>outfile, "Relational operator expected."
    elif num == 21:
        print >>outfile, "Expression must not contain a procedure or function identifier"
    elif num == 22: 
        print >>outfile, "Right parenthesis missing"
    elif num == 23:  
        print >>outfile, "The preceding factor cannot be followed by this symbol."
    elif num == 24:
        print >>outfile, "An expression cannot begin with this symbol."
    elif num ==25:
        print >>outfile, "Constant or Number is expected."
    elif num == 26: 
        print >>outfile, "This number is too large."
    elif num == 27:
        print >>outfile, "Lparen expected."
    elif num == 28:
        print >>outfile, "TO/DOWNTO expected."
    elif num == 29:
        print >>outfile, "DO expected."
    elif num == 30:
        print >>outfile, "UNTIL expected."
    elif num == 31:
        print >>outfile, "OF expected."
    elif num == 32:
        print >>outfile, "Number or Identifer expected."
    elif num == 33:
        print >>outfile, "Colon expected."
    elif num == 34:
        print >>outfile, "Semicolon expected."
    elif num == 35:
        print >>outfile, "CEND expected."
    elif num == 36:
        print >>outfile, "Identifier here must be a function."
    elif num == 37:
        print >>outfile, "Procedure or function expected."
    elif num == 38:
        print >>outfile, "Variable expected. If function, return method must be in its own body."
    elif num == 39:
        print >>outfile, "VAL or REF expected."
    exit(0)
#---------GET CHARACTER FUNCTION-------------------------------------------------------------------
def getch():
    global  whichChar, ch, linelen, line;
    if whichChar == linelen:         #if at end of line
        whichChar = 0
        line = infile.readline()     #get next line
        linelen = len(line)
        sys.stdout.write(line)
    if linelen != 0:
        ch = line[whichChar]
        whichChar += 1
    return ch
#----------GET SYMBOL FUNCTION---------------------------------------------------------------------
def getsym():
    global charcnt, ch, al, a, norw, rword, sym, nmax, id, num
    while ch == " " or ch == "\n" or ch == "\r":
        getch()
    a = []
    if ch.isalpha():
        k = 0
        while True:
            a.append(string.upper(ch))
            getch()
            if not ch.isalnum():
                break
        id = "".join(a)
        flag = 0
        for i in range(0, norw):
            if rword[i] == id:
                sym = rword[i]
                flag = 1
        if  flag == 0:    #sym is not a reserved word
            sym = "ident"
    elif ch.isdigit():
        k=0
        num=0
        sym = "number"
        while True:
            a.append(ch)
            k += 1
            getch()
            if not ch.isdigit():
                break
        if k>nmax:
            error(30)
        else:
            num = "".join(a)
    elif ch == ':':
        getch()
        if ch == '=':
            sym = "becomes"
            getch()
        else:
            sym = "colon"
    elif ch == '>':
        getch()
        if ch == '=':
            sym = "geq"
            getch()
        else:
            sym = "gtr"
    elif ch == '<':
        getch()
        if ch == '=':
            sym = "leq"
            getch()
        elif ch == '>':
            sym = "neq"
            getch()
        else:
            sym = "lss"
    else:
        sym = ssym[ch]
        getch()
#--------------POSITION FUNCTION----------------------------
def position(tx, id):
    global  table;
    table[0] = tableValue(id, "TEST", "TEST", "TEST", "TEST", "TEST") # added 7th argument
    i = tx
    while table[i].name != id:
        i=i-1
    return i
#---------------ENTER PROCEDURE-------------------------------
def enter(tx, k, level, dx):
    global id, num, codeIndx;
    tx[0] += 1
    params = []
    while (len(table) > tx[0]):
      table.pop()
    if k == "const":
        x = tableValue(id, k, level, "NULL", num, "NULL")
    # Begin new code
    elif k == "variable" or k == "val" or k == "ref":
        x = tableValue(id, k, level, dx, "NULL", "NULL")
        dx += 1
    # End new code
    elif k == "procedure" or k == "function":
        x = tableValue(id, k, level, dx, "NULL", params)
    table.append(x)
    return dx
#--------------CONST DECLARATION---------------------------
def constdeclaration(tx, level):
    global sym, id, num;
    if sym=="ident":
        getsym()
        if sym == "eql":
            getsym()
            if sym == "number":
                enter(tx, "const", level, "null")
                getsym()
            else:
                error(2)
        else:
            error(3)
    else:
        error(4)
#-------------VARIABLE DECLARATION--------------------------------------
def vardeclaration(tx, level, dx):
    global sym;
    if sym=="ident":
        dx = enter(tx, "variable", level, dx)
        getsym()
    else:
        error(4)
    return dx
#-------------BLOCK-------------------------------------------------------------
def block(tableIndex, level):
    global sym, id, codeIndx, codeIndx0;
    tx = [1]
    tx[0] = tableIndex
    tx0 = tableIndex
    dx = 3
    cx1 = codeIndx
    gen("JMP", 0 , 0)
    while sym == "PROCEDURE" or sym == "VAR" or sym == "CONST" or sym == "FUNCTION" or sym == "lparen": 
        # Begin new code
        if level > 0:
            if sym == "lparen":
                getsym()
                while True:
                    if sym == "VAL" or sym == "REF":
                        savesym = sym
                        getsym()
                    else:
                        error(39)

                    while True:
                        if sym == "ident":
                            if savesym == "VAL":
                                dx = enter(tx, "val", level, codeIndx)
                                table[tx0].params.append(False)
                            if savesym == "REF":
                                dx = enter(tx, "ref", level, codeIndx)
                                table[tx0].params.append(True)
                        else:
                            error(39)
                        getsym()
                        if sym != "comma":
                            break
                        getsym()

                    if sym != "semicolon":
                        break
                    getsym()
                if sym != "rparen":
                    error(22)
                getsym()

            if sym == "semicolon":
                getsym()
            # End new code
        if sym == "CONST":
            while True:               #makeshift do while in python
                getsym()
                constdeclaration(tx, level)
                if sym != "comma":
                    break
            if sym != "semicolon":
                error(10)
            getsym()
        if sym == "VAR":
            while True:
                getsym()
                dx = vardeclaration(tx, level, dx)
                if sym != "comma":
                    break
            if sym != "semicolon":
                error(10)
            getsym()
        # Begin new code (adding support for functions)
        while sym == "PROCEDURE" or sym == "FUNCTION":
            savesym = sym
            getsym()
            if sym == "ident":
                if savesym == "PROCEDURE":
                    enter(tx, "procedure", level, codeIndx)
                if savesym == "FUNCTION":
                    enter(tx, "function", level, codeIndx)
        # End new code
                getsym()
            else:
                error(4)

            # Moved to the top of block for compiler 4
            #if sym != "semicolon":
            #   error(10)
            #getsym()

            block(tx[0], level+ 1)

            if sym != "semicolon":
                error(10)
            getsym()
    fixJmp(cx1, codeIndx)
    if tx0 != 0:
        table[tx0].adr = codeIndx
    codeIndx0 = codeIndx
    print dx
    gen("INT", 0, dx)
    statement(tx[0], level, tx0)
    gen("OPR", 0, 0)
    #print code for this block
    printCode()
#--------------STATEMENT----------------------------------------
def statement(tx, level, tx0):
    global sym, id, num;
    if sym == "ident" or sym == "VAL" or sym == "REF":
        i = position(tx, id)
        if i==0:
            error(11)
        # Begin new code (adding support for functions)
        elif table[i].kind != "variable" and table[i].kind != "function" and table[i].kind != "val" and table[i].kind != "ref":
            error(12)
        kind = table[i].kind
        getsym()
        if sym != "becomes":
            error(13)
        getsym()
        expression(tx, level)
        if kind == "variable" or kind == "VAL":
            gen("STO", level - table[i].level, table[i].adr)
        if kind == "function":
            if i == tx0:
                gen("STO", 0, -1)
            else:
                error(38)
        if kind == "REF":
            gen("STI", level-table[i].level, table[i].adr)
        # End new code

    elif sym == "CALL":
        getsym()
        if sym != "ident":
            error(14)
        i = position(tx, id)
        if i==0:
            error(11)
        if table[i].kind != "procedure" or table[i].kind != "function":
            error(15)
        getsym()
        if sym == "lparen":
            getsym()
            p = 0
            gen("INT", 0, 3)
            while True:
                if table[i].params[p] == true:
                    getsym()
                    if sym != "ident":
                        error(14)
                    if table[i].kind == "variable" or table[i].kind == "VAL":
                        gen("LDA", level - table[i].level, table[i].adr)
                        getsym()
                    else:
                        gen("LOD", level - table[i].level, table[i].adr)
                        getsym()
                else:
                    expression(tx, level)
                p += 1
                getsym()
                if sym != "comma":
                    break


        gen("CAL", level - table[i].level, table[i].adr)
        getsym()

    elif sym == "IF":
        getsym()
        # Begin new code (all conditions change to general expression)
        genex(tx, level)
        # End new code
        cx1 = codeIndx
        gen("JPC", 0, 0)
        if sym != "THEN":
            error(16)
        getsym()
        statement(tx, level, tx0)
        # Begin new code
        fixJmp(cx1, codeIndx)
        if sym == "ELSE":
            cx2 = codeIndx
            gen("JMP", 0, 0)
            fixJmp(cx1, codeIndx)
            getsym()
            statement(tx, level, tx0)
            fixJmp(cx2, codeIndx)
        else:
            fixJmp(cx1, codeIndx)
        # End new code

    elif sym == "BEGIN":
        while True:
            getsym()
            statement(tx, level, tx0)
            if sym != "semicolon":
                break
        if sym != "END":
            error(17)
        getsym()

    elif sym == "WHILE":
        getsym()
        cx1 = codeIndx
        # Begin new code (condition -> general expression)
        genex(tx, level)
        # End new code
        cx2 = codeIndx
        gen("JPC", 0, 0)
        if sym != "DO":
            error(18)
        getsym()
        statement(tx, level, tx0)
        gen("JMP", 0, cx1)
        fixJmp(cx2, codeIndx)

    elif sym == "REPEAT":
        getsym()
        # Begin new code
        cx = codeIndx
        statement(tx, level, tx0)
    	while sym == "semicolon":
            getsym()
            statement(tx, level, tx0)
        if sym != "UNTIL":
            error(30)
        getsym()
        genex(tx, level)  # Condition turns into genex
        gen("JPC", 0, cx)
        # End new code

    elif sym == "FOR":
            getsym()
            if sym != "ident":
                error(14)
            i = position(tx, id)
            if (i == 0):
                error(11)
            elif (table[i].kind != "variable"):
                error(15)
            getsym()
            if sym != "becomes":
                error(13)
            getsym()
            expression(tx, level)
            
            # Begin new code
            gen("STO", level-table[i].level, table[i].adr)
            if sym != "TO" and sym != "DOWNTO":
                error(28)
            savesym = sym
            getsym()
            expression(tx, level)
            cx1 = codeIndx
            gen("CTS", 0, 0)
            gen("LOD", level-table[i].level, table[i].adr)
            if savesym == "TO":
                gen("OPR", 0, 11)
            if savesym == "DOWNTO":
                gen("OPR", 0, 13)
            cx2 = codeIndx
            gen("JPC", 0, 0)
            if sym != "DO":
                error(18)
            getsym()
            statement(tx, level, tx0)
            gen("LOD", level-table[i].level, table[i].adr)
            gen("LIT", 0, 1)
            if savesym == "TO":
                gen("OPR", 0, 2)
            if savesym == "DOWNTO":
                gen("OPR", 0, 3)
            gen("STO", level-table[i].level, table[i].adr)
            gen("JMP", 0, cx1)
            fixJmp(cx2, codeIndx)
            gen("INT", 0, -1)
            # End new code

    elif sym == "CASE":
            getsym()
            expression(tx, level)
            if sym != "OF":
                error(31)
            getsym()
            casenum = 0 # Used to keep track of # of cases, referenced later
            while sym == "number" or sym == "ident":
                if sym == "ident":
                    i = position(tx, id)
                    if (i == 0):
                        error(11)
                    elif (table[i].kind != "const"):
                        error(15)

                # Begin new code
                gen("CTS", 0, 0)
                if sym == "number":
                    gen("LIT", 0, num)
                if sym == "ident":
                    gen("LIT", 0, table[i].value)
                gen("OPR", 0, 8)
                cx1 = codeIndx
                gen("JPC", 0, 0)
                # End new code

                getsym()
                if sym != "colon":
                    error(33)
                getsym()
                statement(tx, level, tx0)
                if sym != "semicolon":
                    error(34)
                getsym()

                # Begin new code
                if casenum == 0: # In order to keep track of which case, we make a counter
                    cx2 = codeIndx
                    gen("JMP", 0, 0)
                else:
                    gen("JMP", 0, cx2)
                fixJmp(cx1, codeIndx)
                casenum += 1
                # End new code

            if sym != "CEND":
                error(35)
            getsym()
            fixJmp(cx2, codeIndx)
            gen("INT", 0, -1)


    elif sym == "WRITE" or sym == "WRITELN":
            # Begin new code
            savesym = sym
            getsym()
            if sym != "lparen":
                error(27)
            while True:
                getsym()
                expression(tx, level)
                gen("OPR", 0, 14)
                if sym != "comma":
                    break
            if sym != "rparen":
                error(22)
            getsym() 
            if savesym == "WRITELN":
                gen("OPR", 0, 15)
            # End new code

#--------------EXPRESSION--------------------------------------
def expression(tx, level):
    global sym;
    if sym == "plus" or sym == "minus": 
        addop = sym
        getsym()
        term(tx, level)
        if (addop == "minus"):         #if minus sign, do negate operation
            gen("OPR", 0, 1)
    else:
        term(tx, level)
    
    # Begin new code (Adding support for "OR")
    while sym == "plus" or sym == "minus" or sym == "OR":
        addop = sym
        getsym()
        term(tx, level)
        
        if(addop == "minus"):
            gen("OPR", 0, 3)       #subtract operation
        else:
            gen("OPR", 0, 2)       #add operation
    # End new code  
#-------------TERM----------------------------------------------------
def term(tx, level):
    global sym;
    factor(tx, level)

    # Begin new code (Adding support for "AND")
    while sym=="times" or sym=="slash" or sym == "AND":
        mulop = sym
        getsym()
        factor(tx, level)
        if mulop == "slash":
            gen("OPR", 0, 5)         #divide operation
        else:
            gen("OPR", 0, 4)         #multiply operation
    # End new code
#-------------FACTOR--------------------------------------------------
def factor(tx, level):
    global sym, num, id;
    if sym == "ident":
        i = position(tx, id)
        if i==0:
            error(11)
        if table[i].kind == "const":
            gen("LIT", 0, table[i].value)
        # Begin new code compiler 4
        elif table[i].kind == "variable" or table[i].kind == "val":
            gen("LOD", level-table[i].level, table[i].adr)
        elif table[i].kind == "ref":
            gen("LDI", level-table[i].level, table[i].adr)
        # End new code
        # Begin new code (Adding support for functions) compiler 3
        elif table[i].kind == "procedure" or table[i].kind == "function":
            error(21)
        # End new code
        getsym()
    elif sym == "number":
        gen("LIT", 0, num)
        getsym()
    elif sym == "lparen":
        getsym()
        genex(tx, level) # This is now considered a general expression
        if sym != "rparen":
            error(22)
        getsym()
    # Begin new code (support for CALL and NOT added here)
    elif sym == "CALL":
        getsym()
        if sym == "ident":
            i = position(tx, id)
            if i==0:
                error(11)
            elif table[i].kind != "function":
                error(37)
            gen("INT", 0, 1)
            ###############################
            getsym()
            if sym == "lparen":
                getsym()
                p = 0
                gen("INT", 0, 3)
                while True:
                    if table[i].params[p] == True:
                        getsym()
                        if sym != "ident":
                            error(14)
                        if table[i].kind == "variable" or table[i].kind == "VAL":
                            gen("LDA", level - table[i].level, table[i].adr)
                        else:
                            gen("LOD", level - table[i].level, table[i].adr)
                        getsym()
                    else:
                        expression(tx, level)
                    p += 1
                    if sym != "comma":
                        break
            ################################

            gen("CAL", level-table[i].level, table[i].adr)
            getsym()
        else:
            error(4)
        
    elif sym == "NOT":
        getsym()
        factor(tx, level)
        gen("LIT", 0, 0)
        gen("OPR", 0, 8)
    # End new code
    else:
        error(24)
    

#-----------GENERAL EXPRESSION-------------------------------------------------
def genex(tx, level): # Used to be condition, now genex (general expression)
    global sym;
    if sym == "ODD":
        getsym()
        expression(tx, level)
        gen("OPR", 0, 6)
    else:
        expression(tx, level)
        if (sym in ["eql","neq","lss","leq","gtr","geq"]):
            temp = sym
            getsym()
            expression(tx, level)
            if temp == "eql":
                gen("OPR", 0, 8)
            elif temp == "neq":
                gen("OPR", 0, 9)
            elif temp == "lss":
                gen("OPR", 0, 10)
            elif temp == "geq":
                gen("OPR", 0, 11)
            elif temp == "gtr":
                gen("OPR", 0, 12)
            elif temp == "leq":
                gen("OPR", 0, 13)
#-------------------MAIN PROGRAM------------------------------------------------------------#
rword.append('AND')
rword.append('BEGIN')
rword.append('CALL')
rword.append('CASE')
rword.append('CEND')
rword.append('CONST')
rword.append('DO')
rword.append('DOWNTO')
rword.append('ELSE')
rword.append('END')
rword.append('FOR')
rword.append('FUNCTION')
rword.append('IDENT')
rword.append('IF')
rword.append('NOT')
rword.append('NUMBER')
rword.append('ODD')
rword.append('OF')
rword.append('OR')
rword.append('PROCEDURE')
rword.append('REF') # New Rword
rword.append('REPEAT')
rword.append('THEN')
rword.append('TO')
rword.append('UNTIL')
rword.append('VAR')
rword.append('VAL')
rword.append('WHILE')
rword.append('WRITE')
rword.append('WRITELN')

ssym = {'+' : "plus",
             '-' : "minus",
             '*' : "times",       
             '/' : "slash",
             '(' : "lparen",
             ')' : "rparen",
             '=' : "eql",
             ',' : "comma",
             '.' : "period",
             '#' : "neq",
             '<' : "lss",
             '>' : "gtr",
             '"' : "leq",
             '@' : "geq",
             ';' : "semicolon",
             ':' : "colon",}
charcnt = 0
whichChar = 0
linelen = 0
ch = ' '
kk = al                
a = []
id= '     '
errorFlag = 0
table.append(0)    #making the first position in the symbol table empty
sym = ' '       
codeIndx = 0         #first line of assembly code starts at 1
prevIndx = 0
infile =    sys.stdin       #path to input file
outfile =  sys.stdout     #path to output file, will create if doesn't already exist

getsym()            #get first symbol
block(0, 0)             #call block initializing with a table index of zero
if sym != "period":      #period expected after block is completed
    error(9)
print  
if errorFlag == 0:
    print >>outfile, "Successful compilation!\n"
    
Interpret()
