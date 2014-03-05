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
                            # LISP doesn't need SQBRACKETS - remove this
OPENSQBRACKET   = 60
CLOSESQBRACKET  = 70
PLUS            = 35
MINUS           = 45
DIVISION        = 55
MULTIPLICATION  = 65

# Keywords
KW_CAR          = 80
KW_CDR          = 90

UNKNOWN         = 0

nl_SEXP         = 105

nl_CAR          = 200
nl_CDR          = 210

names   = []

# right now, nl_CAR, nl_CDR and everything else creates Sexpressions

grammar = [
            [nl_SEXP,  OPENBRACKET,    NUMBER,     DOT,        NUMBER,         CLOSEBRACKET],
            [nl_SEXP,  OPENBRACKET,    nl_SEXP,    DOT,        NUMBER,         CLOSEBRACKET],
            [nl_SEXP,  OPENBRACKET,    nl_SEXP,    DOT,        nl_SEXP,        CLOSEBRACKET],
            [nl_SEXP,  OPENBRACKET,    NUMBER,     DOT,        nl_SEXP,        CLOSEBRACKET],
            [nl_CAR,  OPENBRACKET,    KW_CAR,     nl_SEXP,    CLOSEBRACKET],
            [nl_CDR,  OPENBRACKET,    KW_CDR,     nl_SEXP,    CLOSEBRACKET]
          ]

# Class Interpreter performs grammar validation and once done calls the 
#   necessary methods to evaluate the 'command'
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
        if type(tok) == type('string'):
            if len(tok) == 1:
                if str.isdigit(tok) == True:
                    return NUMBER
                # possibly a delimiter such as '.' or '(' or '['
                elif tok == '.':
                    return DOT
                elif tok == '(':
                    return OPENBRACKET
                elif tok == ')':
                    return CLOSEBRACKET
                elif tok == '[':
                    return OPENSQBRACKET
                elif tok == ']':
                    return CLOSESQBRACKET
                elif tok == '+':
                    return PLUS
                elif tok == '-':
                    return MINUS
                elif tok == '/':
                    return DIVISION
                elif tok == '*':
                    return MULTIPLICATION
                elif tok >= 'A' and tok <= 'Z':
                    return NAME
            elif tok == 'CAR':
                return KW_CAR
            elif tok == 'CDR':
                return KW_CDR
            else:
                global names
                names = names + [tok]
                return NAME
        else:
            return UNKNOWN
    # end of tokType()

    #####################################
    # Function : 'evaluate'
    #   Parameter   : 
    #   Returns     : 
    #####################################
    def evalList(self, expToks):

        from Sexp import Sexp
        
        if expToks[0][1] == CLOSEBRACKET:
            return NILt

        if expToks[1][1] == CLOSEBRACKET:
            sexp = Sexp()
            sexp.cons(expToks[0], NILt)
            return (sexp, nl_SEXP)

        sexp = Sexp()
        sexp.cons(expToks[0], self.evalList(expToks[1:]))
        return (sexp, nl_SEXP)
    # end of evalList()

    #####################################
    # Function : 'evaluate'
    #   Parameter   : 
    #   Returns     : 
    #####################################
    def evaluate(self, expToks):

        from Sexp import Sexp

        # expToks is a list of tuples (token, toketype)
        # evaluate should make sure that expToks is valid
        # and evaluate them

        # check whether expToks represents a list
        if expToks[0][1] == OPENBRACKET and                 \
            expToks[len(expToks)-1][1] == CLOSEBRACKET:
            listFailed = False
            for x in expToks:
                if x[1] != NUMBER       and \
                    x[1] != NAME        and \
                    x[1] != T           and \
                    x[1] != NIL         and \
                    x[1] != nl_SEXP     and \
                    x[1] != KW_CAR      and \
                    x[1] != KW_CDR      and \
                    x[1] != PLUS        and \
                    x[1] != MINUS       and \
                    x[1] != DIVISION    and \
                    x[1] != MULTIPLICATION and \
                    x[1] != OPENBRACKET and \
                    x[1] != CLOSEBRACKET:

                    listFailed = True
                    break
                # end if
            # end for
            if listFailed == False:
                return self.evalList(expToks[1:])
        # end if

        for x in grammar:
            if(len(expToks) == len(x)-1):
                doesntMatch = False
                for y in xrange(len(expToks)):
                    if expToks[y][1] != x[y+1]:
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
                    sexp.cons(expToks[1], expToks[3])
                # elif x[0] == nl_CAR:
                #     toReturn = expToks[2][0].car
                #     if type(toReturn) == str:
                #         return (toReturn, NUMBER)
                #     else:
                #         return (toReturn, nl_SEXP)
                # elif x[0] == nl_CDR:
                #     toReturn = expToks[2][0].cdr
                #     if type(toReturn) == str:
                #         return (toReturn, NUMBER)
                #     else:
                #         return (toReturn, nl_SEXP)
                # end of if-elif
                return (sexp, nl_SEXP)
            # end if
            # return NULLSexp
        # end for

        # return NULLSexp
        return False

    # end of evaluate()


    ################################
    # Function : 'simplifyTokens'
    #   Parameter   : list of tokens
    #   Returns     : simplified
    ################################
    def simplifyTokens(self, tokList):
        # the idea is to pop from the tokens as a queue
        # and whenever a closed bracket occurs, pop until
        # an open bracket and then simplify whatever has
        # popped
        popped = []
        while len(tokList) >-1:

            if len(tokList) == 0:
                print "tokList parsed completely"
                break
            # end if
            popped.append(tokList.pop(0))

            if popped[len(popped)-1][1] == CLOSEBRACKET:

                # pop from popped[] until you get an OPENBRACKET
                toSimplify = []
                toSimplify.insert(0, popped.pop())

                while toSimplify[0][1] != OPENBRACKET:
                    toSimplify.insert(0, popped.pop())

                # toSimplify has the expression that has to be simplified
                sexpTuple = self.evaluate(toSimplify)
                popped.append(sexpTuple)
            # end of if
        # end of while

        return popped[0]
    # end of simplifyTokens()


    #######################################################
    # Function : 'bracketImbalance'
    #   Parameter   : list of tokens
    #   Returns     : 'True' if imbalance in brackets exists
    #                 'False' if everything is good
    ########################################################
    def bracketImbalance(self, tokList):
        NetBrackets     = 0
        NetSqBrackets   = 0

        for x in tokList:
            if x[1] == OPENBRACKET:
                NetBrackets += 1
            elif x[1] == CLOSEBRACKET:
                NetBrackets -= 1
            elif x[1] == OPENSQBRACKET:
                NetSqBrackets += 1
            elif x[1] == CLOSESQBRACKET:
                NetSqBrackets -= 1
            if NetBrackets < 0 or NetSqBrackets < 0:
                print "There is an imbalance in your brackets"
                return True
                break

        # add something to check dot imbalance        

        if NetBrackets != 0 or NetSqBrackets != 0:
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

        splitCommand = command.replace('(',' ( ').replace(')',' ) ').replace('.',' . ').split()

        for x in splitCommand:
            self.tokens = self.tokens + [(x, self.tokType(x))]

        if self.bracketImbalance(self.tokens) == True:
            print "Error : Malformed Syntax"

        else:
            print "Syntax OK"
            simplified = self.simplifyTokens(self.tokens)
            if simplified[1] == NUMBER:
                self.output = simplified[0]
                print "RESULT atom : ", simplified[0]
            elif simplified[1] == nl_SEXP:
                self.output = simplified[0].printSexp()
                print "RESULT sexp : ", simplified[0].printSexp()
            elif simplified[1] == NIL:
                self.output = "NIL"
                print "RESULT sexp : NIL"
    # end of parse()

    ################################
    # Function : '__init__'
    #   Parameter   : 
    #   Returns     : 
    ################################
    def __init__(self, command):
        names = []
        self.parse(command)
    # end of __init__()

# end of class Interpreter

