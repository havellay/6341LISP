NUMBER         = 10
NAME           = 20

# Delimiters
DOT            = 30
OPENBRACKET    = 40
CLOSEBRACKET   = 50
OPENSQBRACKET  = 60
CLOSESQBRACKET = 70

# Keywords
KW_CAR         = 80
KW_CDR         = 90

UNKNOWN        = 0

nl_SEXP        = 105
nl_SEXP1       = 100
nl_SEXP2       = 110
nl_SEXP3       = 120
nl_SEXP4       = 130

# nl_SEXP1 -> means create an Sexp. So, call Sexp.NdotN()
# nl_SEXP2 -> means create an Sexp. So, call Sexp.SdotN()
# nl_SEXP3 -> means create an Sexp. So, call Sexp.SdotS()
# nl_SEXP4 -> means create an Sexp. So, call Sexp.NdotS()

grammar = [
            [nl_SEXP1, OPENBRACKET, NUMBER, DOT, NUMBER, CLOSEBRACKET],
            [nl_SEXP2, OPENBRACKET, nl_SEXP, DOT, NUMBER, CLOSEBRACKET],
            [nl_SEXP3, OPENBRACKET, nl_SEXP, DOT, nl_SEXP, CLOSEBRACKET],
            [nl_SEXP4, OPENBRACKET, NUMBER, DOT, nl_SEXP, CLOSEBRACKET]
          ]
