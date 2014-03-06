# LISP INTERPRETER FOR CSE 6341
# author    : Karpaka Vellaya Haribabu
# email     : karpakavellaya.1@osu.edu
#

# This version of the LISP interpreter displays
# the Parse tree formed from the user's input
# the tree is not evaluated by the Interpreter
# at the moment


import sys

sexpdebug       = False
                    # 1 2 3 4 unused #

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

names   =   []

# make sure that (car.1) and things are valid for this submission


grammar =   [
                [nl_SEXP,  OPENBRACKET,    VAR | KEYWORD,     DOT,        VAR | KEYWORD,         CLOSEBRACKET]
            ]

# Class Sexp
############################################################################
class Sexp :
    # Member variables of 'class Sexp'
    car = 0
    cdr = 0

    def cons(self, tok1, tok2):
        self.car = tok1[0]
        self.cdr = tok2[0]
        if sexpdebug == True:
            print "DEBUG INFORMATION : created Sexp ", self.printSexp()
        return self

    def printSexp(self):
        string = "("
        if type(self.car) is str:
            string = string + self.car
        else:
            string = string + self.car.printSexp() 

        string = string + " . "

        if type(self.cdr) is str:
            string = string + self.cdr
        else:
            string = string + self.cdr.printSexp()
        
        string = string + ")"
        return string

    def __init__(self):
        car = 0
        cdr = 0
    # end of __init__()

# end of class Sexp

