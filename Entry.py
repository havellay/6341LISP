# LISP INTERPRETER FOR CSE 6341
# author    : Karpaka Vellaya Haribabu
# email     : karpakavellaya.1@osu.edu
#

# This version of the LISP interpreter displays
# the Parse tree formed from the user's input
# the tree is not evaluated by the Interpreter
# at the moment

# entry point of the program
############################

if __name__=="__main__":

    import sys

    from Interpreter import Interpreter

    netBracket = 0
    z = ""
    x = ""
    dotAllowed = False
    dotProblem = False
    someError = False
    
    print "Enter ctrl+D to exit from the prompt"
    while netBracket >= 0 and dotProblem == False:
        z = raw_input('~ ')
        x = x+z

        netBracket = 0
        for y in x:
            if y == '(':
                netBracket+=1
            elif y == ')':
                netBracket-=1
            elif y == '.':
                if dotAllowed == False:
                    dotProblem = True
                dotAllowed = False
            else:
                dotAllowed = True
            if netBracket < 0:
                break

        if netBracket == 0 and dotProblem == False:
            x = x.replace('(',' ( ').replace(')',' ) ').replace('.',' . ')
            x = " ".join(x.split())
            oParser = Interpreter(x)
            if oParser.output == "":
                someError = True
                break
            print ">>\"{}\"\n>>> \"{}\"\n".format(x, oParser.output)
            x = ""

    if someError == True:
        someError = True
    elif dotProblem == True:
        print "A problem with dots in your input"
    else:
        print "improper number of brackets : BYE! "
    
# end of entry point
