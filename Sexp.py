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

KEYWORD         = KW_CAR | KW_CDR   # KEYWORDS are only CAR and CDR, which return atoms ?

UNKNOWN         = 0

names   =   [
                'CAR',
                'CDR',
                'CONS'
            ]

grammar =   [
                [nl_SEXP,  OPENBRACKET,    VAR | KEYWORD,     DOT,        VAR | KEYWORD,         CLOSEBRACKET]
            ]

functions   =   [
                    ('CAR',     1),             # PRIMITIVE1
                    ('CDR',     2),             # PRIMITIVE2
                    ('CONS',    3)              # PRIMITIVE3
                ]

# Class Sexp
############################################################################

sexpdebug       = False
                    # 1 2 3 4 unused #

class Sexp :
    # Member variables of 'class Sexp'
    car = 0
    cdr = 0

    def make(self, tok1, tok2):
        self.car = tok1[0]
        self.cdr = tok2[0]
        if sexpdebug == True:
            print "DEBUG INFORMATION : created Sexp ", self.toString()
        return self


    def toString(self):
        string = "("
        if type(self.car) is str:
            string = string + self.car
        else:
            string = string + self.car.toString() 

        string = string + " . "

        if type(self.cdr) is str:
            string = string + self.cdr
        else:
            string = string + self.cdr.toString()
        
        string = string + ")"
        return string
    # print end of toString


    def processFunc(self, func, argSexp):
        print "processFunc : ", self.car
        if type(func) == int:
            if func == 1:
                # PRIMITIVE1 : CAR

                if type(argSexp) != type(self):
                    # FAIL : CAR's argument is not an Sexp
                    return False
                arg1 = argSexp.car
                if type(arg1) != type(self):
                    arg1 = arg1.processSexp()

                arg1 = argSexp.car.processSexp()

                # if type(arg1) == type(self)                     \
                #     and type(argSexp.cdr) != type(self)         \
                #     and argSexp.cdr == 'NIL'                    \
                #     and type(arg1.car) != type(self):
                    
                    # returning a string
                return arg1.car

            elif func == 2:
                # PRIMITIVE2 : CDR

                if type(argSexp) != type(self):
                    # FAIL : CAR's argument is not an Sexp
                    return False
                arg1 = argSexp.car
                if type(arg1) == type(self):
                    arg1 = arg1.processSexp()

                # if type(arg1) == type(self)                     \
                #     and type(argSexp.cdr) != type(self)         \
                #     and argSexp.cdr == 'NIL'                    \
                #     and type(arg1.cdr) != type(self):
                    
                    # returning a string
                return arg1.cdr

            elif func == 3:
                # PRIMITIVE3 : CONS

                if type(argSexp) != type(self):
                    return False
                arg1 = argSexp.car
                if type(arg1) == type(self):
                    arg1 = arg1.processSexp()
                
                if type(argSexp.cdr) != type(self):
                    return False
                arg2 = argSexp.cdr.car
                if type(arg2) == type(self):
                    arg2 = arg2.processSexp()

                # print type(arg1) != type(self)
                # print type(argSexp.cdr) == type(self)
                # print type(arg2) != type(self)
                # print type(argSexp.cdr.cdr) == str
                # print argSexp.cdr.cdr == 'NIL'

                # if type(arg1) != type(self)                     \
                #     and type(argSexp.cdr) == type(self)         \
                #     and type(arg2) != type(self)                \
                #     and type(argSexp.cdr.cdr) == str            \
                #     and argSexp.cdr.cdr == 'NIL':
                    
                toreturn = Sexp()
                toreturn.make((arg1,0), (arg2,0))
                return toreturn

    # end processFunc


    def processSexp(self):

        print "processSexp : ", self.car, self.cdr
        
        if type(self.car) == type(self):
            # car is an Sexp, have to process it to continue

            output = self.car.processSexp()
            print "returning processSexp : ", self.car, self.cdr, output
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
                    print "returning processSexp : ", self.car, self.cdr, output
                    return output

            ## arguments of self.car is in the sexp self.cdr

        else:
            # self.car is an atom
            # add checks for NIL and T

            print "CAR is an atom {}".format(self.car)

        # end if


        if type(self.cdr) == type(self):
            # self.cdr is an Sexp, this will be the 
            # argument for the function in self.car

            output = self.cdr.processSexp()
            print "returning processSexp : ", self.car, self.cdr, output
            return output

        elif type(self.cdr) == str:
            # cdr is either a variable or a function call

            for x in functions:
                if x[0] == self.car:
                    output = self.processFunc(x[1], self.cdr)
                    print "returning processSexp : ", self.car, self.cdr, output
                    return output

        else:
            print "CDR is an atom {}".format(self.cdr)
            
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

