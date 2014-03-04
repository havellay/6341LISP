import sys

T               = 5
NUMBER          = 10
NAME            = 20
NIL             = 25

Tt              = ('T', T)
NILt            = ('NIL', NIL)

# Delimiters
DOT             = 30
OPENBRACKET     = 40
CLOSEBRACKET    = 50
OPENSQBRACKET   = 60
CLOSESQBRACKET  = 70

# Keywords
KW_CAR          = 80
KW_CDR          = 90

UNKNOWN         = 0

nl_SEXP         = 105
nl_SEXP1        = 100
nl_SEXP2        = 110
nl_SEXP3        = 120
nl_SEXP4        = 130

nl_CAR          = 200
nl_CDR          = 210

# nl_SEXP1 -> means create an Sexp. So, call Sexp.NdotN()
# nl_SEXP2 -> means create an Sexp. So, call Sexp.SdotN()
# nl_SEXP3 -> means create an Sexp. So, call Sexp.SdotS()
# nl_SEXP4 -> means create an Sexp. So, call Sexp.NdotS()

grammar = [
            [nl_SEXP,  OPENBRACKET,    NUMBER,     DOT,        NUMBER,         CLOSEBRACKET],
            [nl_SEXP,  OPENBRACKET,    nl_SEXP,    DOT,        NUMBER,         CLOSEBRACKET],
            [nl_SEXP,  OPENBRACKET,    nl_SEXP,    DOT,        nl_SEXP,        CLOSEBRACKET],
            [nl_SEXP,  OPENBRACKET,    NUMBER,     DOT,        nl_SEXP,        CLOSEBRACKET],
            [nl_CAR,   OPENBRACKET,    KW_CAR,     nl_SEXP,    CLOSEBRACKET],
            [nl_CDR,   OPENBRACKET,    KW_CDR,     nl_SEXP,    CLOSEBRACKET]
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
        return self

    def printSexp(self):
        string = " ( "
        if type(self.car) == str:
            string = string + self.car
        else:
            string = string + self.car.printSexp() 

        string = string + " . "

        if type(self.cdr) == str:
            string = string + self.cdr
        else:
            string = string + self.cdr.printSexp()
        
        string = string + " ) "
        return string

    def __init__(self):
        car = 0
        cdr = 0
    # end of __init__()

# end of class Sexp

