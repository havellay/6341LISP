# entry point of the program
############################

if __name__=="__main__":

    import sys

    from Interpreter import Interpreter

    # command = sys.argv[1:]
    command = "(CAR(1.(2.3)))"      # giving just a sample string now, have
                                    # to change this and take input from
                                    # stdin
    oParser = Interpreter(command)
    print "for Input \"{}\" Output \"{}\"".format(command, oParser.output)

    command = "(CDR((1.2).3))"
    oParser = Interpreter(command)
    print "for Input \"{}\" Output \"{}\"".format(command, oParser.output)

    command = "(CAR((1.2).3))"
    oParser = Interpreter(command)
    print "for Input \"{}\" Output \"{}\"".format(command, oParser.output)

    command = "( (2.3) (2.3) )"
    oParser = Interpreter(command)
    print "for Input \"{}\" Output \"{}\"".format(command, oParser.output)

# end of entry point
