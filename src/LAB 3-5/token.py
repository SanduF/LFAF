class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'
    keywords = {
        "and":       "AND",
        "as":        "AS",
        "assert":    "ASSERT",
        "break":     "BREAK",
        "class":     "CLASS",
        "continue":  "CONTINUE",
        "def":       "FUNCTION",
        "del":       "DEL",
        "elif":      "ELIF",
        "else":      "ELSE",
        "except":    "EXCEPT",
        "False":     "FALSE",
        "finally":   "FINALLY",
        "for":       "FOR",
        "from":      "FROM",
        "global":    "GLOBAL",
        "if":        "IF",
        "import":    "IMPORT",
        "in":        "IN",
        "is":        "IS",
        "lambda":    "LAMBDA",
        "len":       "LEN",
        "None":      "NONE",
        "nonlocal":  "NONLOCAL",
        "not":       "NOT",
        "or":        "OR",
        "pass":      "PASS",
        "raise":     "RAISE",
        "return":    "RETURN",
        "range" :    "RANGE",
        "True":      "TRUE",
        "try":       "TRY",
        "while":     "WHILE",
        "with":      "WITH",
        "yield":     "YIELD"}
