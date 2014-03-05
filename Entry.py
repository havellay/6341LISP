# entry point of the program
############################

if __name__=="__main__":

    import sys

    from Interpreter import Interpreter

    inputSet = [
                    "(CAR(1.(2.3)))",
                    "(CDR((1.2).3))",
                    "(())",
                    "()",
                    "(+A)"
               ]

    for x in inputSet:
        # command = sys.argv[1:]
        # command = x                   
                                        # giving just a sample string now, have
                                        # to change this and take input from
                                        # stdin
        oParser = Interpreter(x)
        print "for Input \"{}\" Output \"{}\"".format(x, oParser.output)

# end of entry point
