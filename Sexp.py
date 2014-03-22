# LISP INTERPRETER FOR CSE 6341
# author    : Karpaka Vellaya Haribabu
# email     : karpakavellaya.1@osu.edu
#

# This version of the LISP interpreter displays
# the Parse tree formed from the user's input
# the tree is not evaluated by the Interpreter
# at the moment


import sys

T               = 1<<5
Ttup            = ('T', T)

NIL             = 1<<6
NILtup          = ('NIL', NIL)

NUMBER          = 1<<7
NAME            = 1<<8
nl_SEXP         = 1<<9

VAR             = T | NIL | NUMBER | NAME | nl_SEXP

                    # 10 11 unused #

# Delimiters
DOT             = 1<<12
OPENBRACKET     = 1<<13
CLOSEBRACKET    = 1<<14

SPECIALSYMBOL   = DOT | OPENBRACKET | CLOSEBRACKET

                    # 15 unused #

# Keywords
KW_CAR          = 1<<16
KW_CDR          = 1<<17

KEYWORD         = KW_CAR | KW_CDR   # KEYWORDS are only CAR and CDR,
                                    # which return atoms ?

UNKNOWN         = 0

names   =   [
                'CAR',
                'CDR',
                'CONS',
                'ATOM',
                'NULL',
                'EQ',
                'PLUS',
                'MINUS',
                'QUOTIENT',
                'REMAINDER',
                'TIMES',
                'DEFUN',
                'COND',
                'QUOTE',
                'INT',
                'T',
                'NIL'
            ]

grammar =   [
                [nl_SEXP,  OPENBRACKET,    VAR | KEYWORD,     DOT,        VAR | KEYWORD,         CLOSEBRACKET]
            ]

functions   =   [
                    # NAME      ID  ALIST   FUNCCODE
                    ('CAR',     1,  0,      0),         # PRIMITIVE1
                    ('CDR',     2,  0,      0),         # PRIMITIVE2
                    ('CONS',    3,  0,      0),         # PRIMITIVE3
                    ('ATOM',    4,  0,      0),         # PRIMITIVE4
                    ('NULL',    5,  0,      0),         # PRIMITIVE5
                    ('EQ',      6,  0,      0),         # PRIMITIVE6
                    ('PLUS',    7,  0,      0),         # PRIMITIVE7
                    ('MINUS',   8,  0,      0),         # PRIMITIVE8
                    ('QUOTIENT',9,  0,      0),         # PRIMITIVE9
                    ('REMAINDER',10, 0,      0),         # PRIMITIVE10
                    ('TIMES',   11, 0,      0),         # PRIMITIVE11
                    ('DEFUN',   12, 0,      0),         # PRIMITIVE12
                    ('COND',    13, 0,      0),         # PRIMITIVE13
                    ('QUOTE',   14, 0,      0),         # PRIMITIVE14
                    ('INT',     15, 0,      0),         # PRIMITIVE15
                    ('T',       16, 0,      0),         # PRIMITIVE16
                    ('NIL',     17, 0,      0)          # PRIMITIVE17
                ]

# Class Sexp
############################################################################

DEBUG       = False
ERROR       = True
                    # 1 2 3 4 unused #

#
# RETURNS : None
#   prints a string
#   based on a flag : make flags as
#   DEBUG | DEBUG or ERROR | ERROR
#
def notifyUser(string, flag):
    if flag == True:
        print string
# end notifyUser

#
# RETURNS : boolean / int
#
#   boolean (False) means Failure
#   int means that the integer was
#   successfully extracted
#
def extractIntFromString(string):

    if string.isdigit() == True:
        return int(string)

    if string[1:].isdigit() == True:
        if string[0] == '+':
            return int(string[1:])
        elif string[0] == '-':
            return -1*int(string[1:])
        else:
            notifyUser("Error 1 : Couldn't extract Integer from "+string, ERROR)
            return False

    notifyUser("Error 2 : Couldn't extract Integer from "+string, ERROR)
    return False
# end of extractIntFromString

class Sexp :
    # Member variables of 'class Sexp'
    car = 0
    cdr = 0

    #
    # RETURNS : Sexp
    #   prints a string
    #
    def make(self, tok1, tok2):
        self.car = tok1[0]
        self.cdr = tok2[0]

        notifyUser("Sexpression created "+self.toString(), DEBUG)

        return self
    # end of make


    #
    # RETURNS : str
    #   and prints a debug string
    #
    #
    def toString(self):

        notifyUser(self+" has car "+self.car+" and cdr "+self.cdr, DEBUG)

        string = "("
        if type(self.car) == type(self):
            string = string + self.car.toString() 
        else:
            string = string + self.car

        string = string + " . "

        if type(self.cdr) == type(self):
            string = string + self.cdr.toString()
        else:
            string = string + self.cdr
        
        string = string + ")"
        return string
    # print end of toString


    #
    # RETURNS : boolean False / Sexp / str
    #                                  ^^^ - atom
    #
    #
    def processFunc(self, func, argSexp):

        notifyUser("processFunc : "+self.car, DEBUG)

        if type(func) != int:
            notifyUser("processFunc called for incorrect function " \
                    +func, DEBUG)
            return False

        if func == 1 or func == 2:
            # Code for CAR and CDR

            if type(argSexp) != type(self):
                    notifyUser("Error : Incorrect parameter for "   \
                            +functions[func-1], ERROR)
                return False

            if func == 1:
                if type(argSexp.car) == type(self):
                    argSexp.car = argSexp.car.processSexp()
            else if func == 2:
                if type(argSexp.cdr) == type(self):
                    argSexp.car = argSexp.car.processSexp()

            if func == 1:
                return argSexp.car.car
            else if func == 2:
                return argSexp.car.cdr

        elif func == 3:
            # Code for CONS

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect parameter for CONS ", \
                        ERROR)
                return False

            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()
            
            if type(argSexp.cdr) != type(self):
                notifyUser("Error : Incorrect number of parameters  \
                        for CONS", ERROR)
                return False

            if type(argSexp.cdr.car) == type(self):
                argSexp.cdr.car = argSexp.cdr.car.processSexp()

            toreturn = Sexp()
            toreturn.make((argSexp.car,0), (argSexp.cdr.car,0))
                          ################## -> 0 in this argument may
                          #                     come back to bite later
            return toreturn

        elif func == 4:
            # Code for ATOM

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect parameter for ATOM ", \
                        ERROR)
                return False

            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()
            
            if type(argSexp.car) == type(self):
                return 'NIL'
            elif type(argSexp.car) == str:
                return 'T'
            else:
                notifyUser("Error : Unrecognized value at ATOM ", ERROR)
                return False

        elif func == 5:
            # code for NULL

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect parameter for NULL", ERROR)
                return False

            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()
            
            if type(argSexp.car) == str and argSexp.car == 'NIL':
                return 'T'
            elif type(argSexp.car) == type(self):
                return 'NIL'
            else:
                notifyUser("Error : Unrecognized value at NULL", ERROR)
                return False

        elif func == 6:
            # code for EQ

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect parameter for EQ", ERROR)
                return False
            
            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()

            if type(argSexp.cdr) != type(self):
                notifyUser("Error : Incorrect number of parameters for EQ")
                return False

            if type(argSexp.cdr.car) == type(self):
                argSexp.cdr.car = argSexp.cdr.car.processSexp()

            if type(argSexp.car) != str or type(argSexp.cdr.car) != str:
                return 'NIL'
            elif argSexp.car == argSexp.cdr.car         \
                    and type(argSexp.cdr.cdr) == str    \
                    and argSexp.cdr.cdr == 'NIL':
                return 'T'
            else:
                return 'NIL'


        elif func == 7:
            # Code for PLUS

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect parameter for PLUS", ERROR)
                return False
            
            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()

            if type(argSexp.cdr) != type(self):
                notifyUser("Error : Incorrect parameter for PLUS", ERROR)
                return False

            if type(argSexp.cdr.car) == type(self):
                argSexp.cdr.car = argSexp.cdr.car.processSexp()

            if type(argSexp.car) == str                                 \
                    and type(argSexp.car) == type(argSexp.cdr.car):

                arg1Int = extractIntFromString(argSexp.car)
                arg2Int = extractIntFromString(argSexp.cdr.car)

                if (type(arg1Int) == bool and arg1Int == False)         \
                        or (type(arg2Int) == bool and arg2Int == False):
                    notifyUser("Error : Non Integer Parameter to PLUS", ERROR)
                    return False
                
                return str(arg1Int + arg2Int)

            notifyUser("Error : Incorrect Parameter for PLUS", ERROR)
            return False

        elif func == 8:
            # Code for MINUS

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect Parameter for MINUS", ERROR)
                return False
            
            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()

            if type(argSexp.cdr) != type(self):
                notifyUser("Error : Incorrect Parameter for MINUS", ERROR)
                return False

            if type(argSexp.cdr.car) == type(self):
                argSexp.cdr.car = argSexp.cdr.car.processSexp()

            if type(argSexp.car) == str                                 \
                    and type(argSexp.car) == type(argSexp.cdr.car):

                arg1Int = extractIntFromString(argSexp.car)
                arg2Int = extractIntFromString(argSexp.cdr.car)

                if (type(arg1Int) == bool and arg1Int == False)         \
                        or (type(arg2Int) == bool and arg2Int == False):
                    notifyUser("Error : Non Integer Parameter to MINUS", ERROR)
                    return False
                
                return str(arg1Int - arg2Int)

            notifyUser("Error : Incorrect Parameter for MINUS", ERROR)
            return False

        elif func == 9:
            # Code for QUOTIENT

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect Parameter for QUOTIENT", ERROR)
                return False
            
            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()

            if type(argSexp.cdr) != type(self):
                notifyUser("Error : Incorrect Parameter for QUOTIENT", ERROR)
                return False

            if type(argSexp.cdr.car) == type(self):
                argSexp.cdr.car = argSexp.cdr.car.processSexp()

            if type(argSexp.car) == str                                 \
                    and type(argSexp.car) == type(argSexp.cdr.car):

                arg1Int = extractIntFromString(argSexp.car)
                arg2Int = extractIntFromString(argSexp.cdr.car)

                if (type(arg1Int) == bool and arg1Int == False)         \
                        or (type(arg2Int) == bool and arg2Int == False):
                    notifyUser("Error : Non Integer Parameter to QUOTIENT", ERROR)
                    return False
                
                if arg2Int == 0:
                    print "ERROR : Division by Zero!!"
                    return False
                
                return str(arg1Int / arg2Int)

            notifyUser("Error : Incorrect Parameter for QUOTIENT", ERROR)
            return False

        elif func == 10:
            # Code for REMAINDER

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect Parameter for REMAINDER", ERROR)
                return False
            
            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()

            if type(argSexp.cdr) != type(self):
                notifyUser("Error : Incorrect Parameter for REMAINDER", ERROR)
                return False

            if type(argSexp.cdr.car) == type(self):
                argSexp.cdr.car = argSexp.cdr.car.processSexp()

            if type(argSexp.car) == str                                 \
                    and type(argSexp.car) == type(argSexp.cdr.car):

                arg1Int = extractIntFromString(argSexp.car)
                arg2Int = extractIntFromString(argSexp.cdr.car)

                if (type(arg1Int) == bool and arg1Int == False)         \
                        or (type(arg2Int) == bool and arg2Int == False):
                    notifyUser("Error : Non Integer Parameter to REMAINDER", ERROR)
                    return False
                
                if arg2Int == 0:
                    print "ERROR : Division by Zero!!"
                    return False
                
                return str(arg1Int % arg2Int)

            notifyUser("Error : Incorrect Parameter for REMAINDER", ERROR)
            return False

        elif func == 11:
            # Code for TIMES

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect Parameter for TIMES", ERROR)
                return False

            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()

            if type(argSexp.cdr) != type(self):
                notifyUser("Error : Incorrect Parameter for TIMES", ERROR)
                return False

            if type(argSexp.cdr.car) == type(self):
                argSexp.cdr.car = argSexp.cdr.car.processSexp()

            if type(argSexp.car) == str                                 \
                    and type(argSexp.car) == type(argSexp.cdr.car):

                arg1Int = extractIntFromString(argSexp.car)
                arg2Int = extractIntFromString(argSexp.cdr.car)

                if (type(arg1Int) == bool and arg1Int == False)         \
                        or (type(arg2Int) == bool and arg2Int == False):
                    notifyUser("Error : Non Integer Parameter to TIMES", ERROR)
                    return False
                
                return str(arg1Int * arg2Int)

            notifyUser("Error : Incorrect Parameter for TIMES", ERROR)
            return False

        elif func == 12:
            # Code for DEFUN
            # has 3 parameters :
            # ( DEFUN NAME (PARAMS ...) (STMTS ...) )

            ## The fist parameter is the name and should be 
            ## returned as an atom. The second parameter is
            ## the list of parameters that the function 
            ## recognizes. The second part is the code of
            ## the function

            # argSexp is a list is of the following structure :
            #                        SEXP
            #                      /      \
            #                     /        \
            #                    /          \
            #               NAME             \
            #                                 \
            #                                  \
            #                                   SEXP2
            #                                  /    \
            #                           ARGLIST       \
            #                                           \
            #                                             \
            #                                               SEXP3
            #                                       FuncCode    NIL
            
            # extract arglist from this tree and store in the tuple
            # in functions and store the code in that tuple as well

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect parameter for DEFUN", ERROR)
                return False

            if type(argSexp.cdr) != type(self):
                # SEXP2 is not an SEXP - user has probably not
                # defined any parameters or code
                notifyUser("Error : Incorrect parameter for DEFUN", ERROR)
                return False

            if type(argSexp.cdr.cdr) != type(self):
                # SEXP3 is not an SEXP, and so, user has probably 
                # not defined any code for the new method
                notifyUser("Error : Incorrect parameter for DEFUN", ERROR)
                return False
            
            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()
                # arg1 has the name of the method that is being defined

            # arg2 is now a list that has the parameters,
            # we don't need to process this now.

            arg3 = argSexp.cdr.cdr.car
            # arg3 is now the list containing the code of new func

            funcId = len(functions)+1
            functions.append((argSexp.car, funcId, argSexp.cdr.car,     \
                    argSexp.cdr.cdr.car))

            notifyUser("New function defined "+functions[funcId-1][0], DEBUG)

            if type(functions[funcId-1][2] == type(self)):
                notifyUser(functions[funcId-1][0]+" params "+       \
                        functions[funcId-1][2].toString(), DEBUG)

            if type(functions[funcId-1][3]) == type(self):
                notifyUser(functions[funcId-1][0]+" code "+         \
                        functions[funcId-1][3].toString(), DEBUG)

            return functions[funcId-1][0]

        elif func == 13:
            # Code for COND

            # The cdr can be an sexp with several sub lists

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect parameter for COND", ERROR)
                return False

            while type(argSexp) == type(self):
                result = self.evaluateCondition(argSexp.car)
                if type(result) == bool:
                    notifyUser("Error : COND condition didn't evaluate      \
                            to T or NIL", ERROR)
                    return False
                elif type(result) == str:
                    if result == 'NIL':
                        argSexp = argSexp.cdr

                    elif result == 'T':
                        if type(argSexp.car.cdr.car) == type(self):
                            return argSexp.car.cdr.car.processSexp()
                        return argSexp.car.cdr.car

                    else :
                        notifyUser("Error : COND condition didn't evaluate  \
                                to T or NIL", ERROR)
                        return False

                        
                elif type(result) == type(self):
                    notifyUser("Error : COND condition didn't evaluate      \
                            to T or NIL", ERROR)
                    return False
                                    
            if argSexp != 'NIL':
                notifyUser("Error : CONDs list not structured correctly",   \
                        ERROR)
                return False

            if argSexp == 'NIL':
                notifyUser("Error : None of the conditions evaluated to     \
                        T or NIL", ERROR)
                return False

            return argSexp

        elif func == 14:
            # PRIMITIVE : QUOTE

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect Parameter for QUOTE", ERROR)
                return False

            if type(argSexp.cdr) != type(str):
                notifyUser("Error : Incorrect Parameter for QUOTE", ERROR)
                return False

            if argSexp.cdr != 'NIL':
                notifyUser("Error : Incorrect Parameter for QUOTE", ERROR)
                return False

            return argSexp.car

        elif func == 15:
            # PRIMITIVE : INT

            if type(argSexp) != type(self):
                notifyUser("Error : Incorrect parameter for INT", ERROR)
                return False

            if type(argSexp.car) == type(self):
                argSexp.car = argSexp.car.processSexp()

            if type(argSexp.car) == type(self):
                return 'NIL'
            elif type(argSexp.car) == str                               \
                    and type(extractIntFromString(argSexp.car)) == int:
                return 'T'
            else:
                return 'NIL'

        elif func == 16:
            # pseudo PRIMITIVE : T
            # this is probably not needed
        
            if type(argSexp) == str and argSexp == 'NIL':
                return self

            if type(argSexp) == type(self):
                notifyUser("Error : Incorrect parameter for T", ERROR)
                return False

        elif func == 17:
            # pseudo PRIMITIVE : NIL
            # this is probably not needed

            if type(argSexp) == str and argSexp == 'NIL':
                return self

            if type(argSexp) == type(self):
                notifyUser("Error : Incorrect parameter for NIL", ERROR)
                return False

        else :

            notifyUser("processing func "+func+" argSexp "              \
                    +argSexp.toString(), ERROR)

            # argSexp has the arguments that the user has supplied
            # we should substitute the occurrences of 
            # functions[func][2] in functions[func][3] with the
            # argSexp
            
            dupCodeSexp = self.duplicateSexp(functions[func-1][3])

            code = self.subArgsWith(dupCodeSexp,                        \
                    functions[func-1][2], argSexp)

            if type(code) == type(self):
                code = code.processSexp()

            return code

        # end if-elif
    # end processFunc


    #
    # RETURNS : Sexp / str / Boolean
    #
    #
    def evaluateCondition(self, s):

        if type(s) != type(self):
            notifyUser("Error : Incorrect COND usage", ERROR)
            return False

        if type(s.car) == type(self):
            s.car = s.car.processSexp()

        if type(s.car) != str:
            notifyUser("Error : COND expression didn't evaluate to T or     \
                    NIL", ERROR)
            return False

        if s.car == 'T':
            return s.car

        # return 'NIL'
        return s.car

    # end of evaluateCondition


    #
    # RETURNS - Sexp
    #
    #
    def duplicateSexp(self, target):

        duplicate = Sexp()

        if type(target.car) == type(target):
            duplicate.car = self.duplicateSexp(target.car)
        elif type(target.car) == str:
            duplicate.car = target.car

        if type(target.cdr) == type(target):
            duplicate.cdr = self.duplicateSexp(target.cdr)
        elif type(target.cdr) == str:
            duplicate.cdr = target.cdr

        return duplicate

    # end duplicateSexp


    #
    # blindly substitute
    #
    #
    def blindSub(self, codeSexp, param, arg):

        # print "blindsub", codeSexp.car
        # print "blindsub", codeSexp.cdr

        if type(codeSexp) == type(self)                 \
                and type(codeSexp.car) == type(self):
            codeSexp.car = self.subs(codeSexp.car, param, arg)

        if type(codeSexp) == type(self)                 \
                and type(codeSexp.car) == type(param)   \
                and codeSexp.car == param:
            # print "substituting ",codeSexp.car
            codeSexp.car = arg
        
        if type(codeSexp) == type(self)                 \
                and type(codeSexp.cdr) == type(param)   \
                and codeSexp.cdr == param:
            codeSexp.cdr = arg

        if type(codeSexp) == type(self)                 \
                and type(codeSexp.cdr) == type(self):
            codeSexp.cdr = self.blindSub(codeSexp.cdr, param, arg)


        # print "leaving blindsub", codeSexp.car
        # print "leaving blindsub", codeSexp.cdr

        return codeSexp


    #
    # RETURNS - Sexp
    #
    #
    def subs(self, codeSexp, param, arg):
        
        # print "sub", codeSexp.car
        # print "sub", codeSexp.cdr

        # meaningful nodes of param are expected to be strings
        # the following code is in that assumption. But it is
        # possible that it is an sexp ression that is porcessed
        # to an atom

        # print "in subs"
        if type(codeSexp) == type(self)                     \
                and type(codeSexp.car) == str               \
                and codeSexp.car == 'QUOTE':
 
            # print "leaving sub", codeSexp.car
            # print "leaving sub", codeSexp.cdr
               
            return codeSexp

        if type(codeSexp) == type(self)                     \
                and type(codeSexp.car) == str:
            # blind substitute in codeSexp.cdr
            # print "subs ignoring ",codeSexp.car
            codeSexp.cdr = self.blindSub(codeSexp.cdr, param, arg)

        if type(codeSexp) == type(self)                   \
                and type(codeSexp.car) == type(self):
            codeSexp.car = self.subs(codeSexp.car, param, arg)
            codeSexp.cdr = self.subs(codeSexp.cdr, param, arg)

        # if type(codeSexp) == type(self)                     \
        #         and type(codeSexp.car) == type(self):


        #     codeSexp.car.cdr = self.subs(codeSexp.car.cdr, param, arg)
        # 
        # if type(codeSexp) == type(self)                     \
        #         and type(codeSexp.car) == type(param)       \
        #         and codeSexp.car == param:      # this condition is a bit
        #                                         # tricky
        #     codeSexp.car = arg
        # 
        # if type(codeSexp) == type(self)                     \
        #         and type(codeSexp.cdr) == type(self):

        #     codeSexp.cdr = self.subs(codeSexp.cdr, param, arg)

        # if type(codeSexp) == type(self)                     \
        #         and type(codeSexp.cdr) == type(param)       \
        #         and codeSexp.cdr == param:
        # 
        #     codeSexp.cdr = arg

        # print "leaving sub", codeSexp.car
        # print "leaving sub", codeSexp.cdr

        return codeSexp
    # end subs


    def subArgsWith(self, codeSexp, paramSexp, argSexp):

        # notifyUser("\nin subArgsWith \n")
        # notifyUser("\nin argSexp is {}\n".format(argSexp.toString()))
        # notifyUser("\nin paramSexp is {}\n".format(paramSexp.toString()))
        # notifyUser("\nin codeSexp is {}\n".format(codeSexp.toString()))

        # argSexp.car and paramSexp are the comparable S-expressions

        arg     = argSexp
        param   = paramSexp

        while type(arg) == type(self)               \
                and type(param) == type(self):

            # print "\nparamter isn't an atom - bug\n"

            if type(arg.car) == type(self):
                arg.car = arg.car.processSexp()

            codeSexp = self.subs(codeSexp, param.car, arg.car)

            param = param.cdr
            arg = arg.cdr

            if type(param) != type(self):
                if type(arg) == type(self):
                    print "ERROR : more args than parameters"
                    return False
                if arg != 'NIL' and param != 'NIL':
                    codeSexp = self.subs(codeSexp, param, arg)
                break

        # end while
        
        if type(arg) != type(param):
            print "we probably have too many parameters"

        # print "substituted code is ", codeSexp.toString()
        return codeSexp
                
    # end subArgsWith


    def processSexp(self):

        print "HARI processSexp ",self.car, self.cdr

        if type(self.car) == type(self):
            print "Hello ", self.car.toString()
        if type(self.cdr) == type(self):
            print "Hello ", self.cdr.toString()

        notifyUser("\nprocessSexp : {}\n".format(self.car, self.cdr))
        
        if type(self.car) == type(self):
            # car is an Sexp, have to process it to continue

            output = self.car.processSexp()

            notifyUser("\nreturning processSexp : {}\n".format(self.car, \
                        self.cdr, output))

            return output

        elif type(self.car) == str:
            # '1', 'NIL', everything is a string now.
            ## car is either a variable or a function call
            ## a condition would go here to check whether
            ## the car is a function call or a variable, for
            ## now, assume that it is a function call

            for x in functions:
                if x[0] == self.car:
                    output = self.processFunc(x[1], self.cdr)

                    notifyUser("\nreturning processSexp : \n"            \
                            .format(self.car, self.cdr, output))

                    return output

            ## arguments of self.car is in the sexp self.cdr

        else:
            # self.car is an atom
            # add checks for NIL and T

            notifyUser("\nCAR is an atom {}\n".format(self.car))

        # end if


        return self
        print "This shouldn't be printed"

        if type(self.cdr) == type(self):
            # self.cdr is an Sexp, this will be the 
            # argument for the function in self.car

            output = self.cdr.processSexp()

            notifyUser("\nreturning processSexp {}\n".format(self.car,   \
                        self.cdr, output))

            return output

        elif type(self.cdr) == str:
            # cdr is either a variable or a function call

            for x in functions:
                if x[0] == self.car:
                    output = self.processFunc(x[1], self.cdr)

                    notifyUser("\nreturning processSexp : {}\n"          \
                            .format(self.car, self.cdr, output))

                    return output

        else:
            notifyUser("CDR is an atom {}".format(self.cdr))
            
        return self
        # end if
        
    # end of processSexp


    #############################################
    # THE FOLLOWING FUNCTIONS MAY NOT BE NEEDED #
    #############################################

    def processArg(self, sexp, num):
        # if sexp.lengthSexp(self) > 1:
        print "in process Arg"
    # end of processArg


    # This function might not be needed
    def lengthSexp(self, typ):

        # think about whether default return value is 0

        ptr = self

        if type(self) == type(typ):
            if type(self.car) == type(self):
                carLength = 1+self.car.lengthSexp(self)
            else:
                carLength = 0

            if type(self.cdr) == type(self):
                cdrLength = 1+self.cdr.lengthSexp(self)
            else:
                cdrLength = 0

            if carLength > cdrLength:
                return carLength

            return cdrLength

        return 0
    # end of lengthSexp()


    def __init__(self):
        car = 0
        cdr = 0
    # end of __init__()

# end of class Sexp

