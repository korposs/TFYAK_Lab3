KEYWORDS = {
    "record",
    "String",
    "int",
    "long",
    "double",
    "float",
    "boolean",
    "char",
    "byte",
    "short",
}

OPERATORS = {
    "==", "!=", "<=", ">=", "&&", "||",
    "=", "<", ">", "+", "-", "*", "/", "!",
}

DELIMITERS = {
    "(", ")", "{", "}", "[", "]",
    ",", ";", ".",
}

TOKEN_TYPES = {
    "KEYWORD":     1,
    "IDENTIFIER":  2,
    "INTEGER":     3,
    "FLOAT":       4,
    "STRING":      5,
    "CHAR":        6,
    "OPERATOR":    7,
    "LPAREN":      8,    # (
    "RPAREN":      9,    # )
    "LBRACE":     10,    # {
    "RBRACE":     11,    # }
    "COMMA":      12,    # ,
    "SEMICOLON":  13,    # ;
    "WHITESPACE": 14,
    "UNKNOWN":    99,
}

DELIMITER_MAP = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ",": "COMMA",
    ";": "SEMICOLON",
}