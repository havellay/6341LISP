# LISP INTERPRETER FOR CSE 6341
# author    : Karpaka Vellaya Haribabu
# email     : karpakavellaya.1@osu.edu
#

# This version of the LISP interpreter displays
# the Parse tree formed from the user's input
# the tree is not mkTreeEvaluated by the Interpreter
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

# Class Interpreter performs grammar validation and once done calls the 
#   necessary methods to mkTreeEvaluate the 'command'
############################################################################
class Interpreter :
    # Member variables of 'class Interpreter'

    # Variable names and literal digits
                            # change the following to use bitwise operations
                            # so, I can do val&ATOM to find if it is an atom
    # Member functions of 'class Interpreter' follow:

    #####################################
    # Function : 'tokType'
    #   Parameter   : a single token
    #   Returns     : 'type' of the Token
    #####################################
    def tokType(self, tok):
        if type(tok) is str:
            if len(tok) == 1:
                if str.isdigit(tok) == True:
                    return NUMBER
                # possibly a delimiter such as '.' or '('
                elif tok == '.':
                    return DOT
                elif tok == '(':
                    return OPENBRACKET
                elif tok == ')':
                    return CLOSEBRACKET
                elif tok >= 'A' and tok <= 'Z':
                    return NAME
                else:
                    # an unrecognized single character
                    # token found
                    return False
            elif tok == 'CAR':
                return KW_CAR
            elif tok == 'CDR':
                return KW_CDR
            else:
                global names
                # '+1 etc. might come here'
                if tok[0] == '+' or tok[0] == '-':
                    if str.isdigit(tok[1:]) == True:
                        return NUMBER
                # '+A' etc. become a possible 'NAME'
                names = names + [tok]
                return NAME
        else:
            return UNKNOWN
    # end of tokType()

    #####################################
    # Function : 'mkTreeEvalList'
    #   Parameter   : 
    #   Returns     : 
    #####################################
    def mkTreeEvalList(self, expToks):

        from Sexp import Sexp
        
        if expToks[0][1] & CLOSEBRACKET:
            return NILtup

        if expToks[1][1] & CLOSEBRACKET:
            sexp = Sexp()
            sexp.make(expToks[0], NILtup)
            return (sexp, nl_SEXP)

        sexp = Sexp()
        sexp.make(expToks[0], self.mkTreeEvalList(expToks[1:]))
        return (sexp, nl_SEXP)
    # end of mkTreeEvalList()

    #####################################
    # Function : 'mkTreeEvaluate'
    #   Parameter   : 
    #   Returns     : 
    #####################################
    def mkTreeEvaluate(self, expToks):

        global names

        from Sexp import Sexp

        # expToks is a list of tuples (token, toketype)
        # mkTreeEvaluate should make sure that expToks is valid
        # and mkTreeEvaluate them

        # check whether expToks represents a list
        if expToks[0][1] & OPENBRACKET and                 \
            expToks[len(expToks)-1][1] & CLOSEBRACKET:
            listFailed = False
            for x in expToks:
                if x[1] & VAR       == 0    and \
                    x[1] & KEYWORD  == 0    and \
                    x[1] != OPENBRACKET     and \
                    x[1] != CLOSEBRACKET:

                    listFailed = True
                    break
                # end if
            # end for
            if listFailed == False:
                var = self.mkTreeEvalList(expToks[1:])
                return var
            # end if
        # end if

        for x in grammar:
            if(len(expToks) == len(x)-1):
                doesntMatch = False
                for y in xrange(len(expToks)):
                    if expToks[y][1] & x[y+1] == 0:
                        doesntMatch = True
                        break
                    # end if
                # end for

                # if we reach here, expToks has the same
                # tokens that the grammar 'y' expects

                # this is a kind of switch case associating
                # x[0] with the function that creates
                # corresponding Sexp

                if doesntMatch == True:
                    continue
                # end if

                sexp = Sexp()

                if x[0] == nl_SEXP:
                    sexp.make(expToks[1], expToks[3])
                # end of if-elif
                return (sexp, nl_SEXP)
            # end if
            # return NULLSexp
        # end for

        return False
    # end of mkTreeEvaluate()


    ################################
    # Function : 'mkTreeSimplifyTokens'
    #   Parameter   : list of tokens
    #   Returns     : simplified
    ################################
    def mkTreeSimplifyTokens(self, tokList):
        # the idea is to pop from the tokens as a queue
        # and whenever a closed bracket occurs, pop until
        # an open bracket and then simplify whatever has
        # popped
        
        popped = []
        while len(tokList) >-1:

            if len(tokList) == 0:
                break
            # end if
            popped.append(tokList.pop(0))

            if popped[len(popped)-1][1] & CLOSEBRACKET:

                # pop from popped[] until you get an OPENBRACKET
                toSimplify = []
                toSimplify.insert(0, popped.pop())

                while toSimplify[0][1] & OPENBRACKET == 0:
                    toSimplify.insert(0, popped.pop())

                # toSimplify has the expression that has to be simplified
                sexpTuple = self.mkTreeEvaluate(toSimplify)
                if type(sexpTuple) is bool and sexpTuple == False:
                    return False
                popped.append(sexpTuple)
            # end of if
        # end of while

        return popped[0]
    # end of mkTreeSimplifyTokens()


    #######################################################
    # Function : 'bracketImbalance'
    #   Parameter   : list of tokens
    #   Returns     : 'True' if imbalance in brackets exists
    #                 'False' if everything is good
    ########################################################
    def bracketImbalance(self, tokList):
        NetBrackets     = 0

        for x in tokList:
            if x[1] & OPENBRACKET:
                NetBrackets += 1
            elif x[1] & CLOSEBRACKET:
                NetBrackets -= 1
            if NetBrackets < 0:
                print "There is an imbalance in your brackets"
                return True
                break

        # add something to check dot imbalance        

        if NetBrackets != 0:
            return True
        return False
    # end of bracketImbalance()


    ################################
    # Function : 'parse'
    #   Parameter   : 
    #   Returns     : 
    ################################
    def parse(self, command):
        self.output = []
        self.tokens = []

        command = command.upper()
        splitCommand = command.replace('(',' ( ').replace(')',' ) ').replace('.',' . ').split()

        for x in splitCommand:
            typeOfToken = self.tokType(x)

            # ugly code to catch corners
            if type(typeOfToken) is bool and typeOfToken == False:
                return False

            self.tokens = self.tokens + [(x, typeOfToken)]

        if self.bracketImbalance(self.tokens) == True:
            print "Error : Malformed Syntax"

        else:
            simplified = self.mkTreeSimplifyTokens(self.tokens)

            # ugly code to catch corners
            if type(simplified) is bool and simplified == False:
                return False

            if simplified[1] & NUMBER:
                self.output = simplified[0]
                # print "RESULT atom : ", simplified[0]
            elif simplified[1] & nl_SEXP:
                self.output = simplified[0].toString()

                # # # # # # # # # S-exp tree is now a 
                # # # # # # # # # Parse Tree.

                processed = simplified[0].processSexp()
                if type(processed) == type(simplified[0]):
                    print processed.toString()
                else:
                    print processed, type(processed)

                # print "RESULT sexp : ", simplified[0].toString()
            else:
                self.output = simplified[0]
                # print "RESULT sexp : ", self.output
            # end if-elif-else

        return True
    # end of parse()

    ################################
    # Function : '__init__'
    #   Parameter   : 
    #   Returns     : 
    ################################
    def __init__(self, command):
        names = []
        anOutput = self.parse(command)
        if type(anOutput) is bool and anOutput == False:
            print "Unexpected token in input"
            self.output = ""
        # end if
    # end of __init__()

# end of class Interpreter

