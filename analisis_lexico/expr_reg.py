TOKEN_REGEX = [
    # Palabras Reservadas (1-30)
    (2, "CLASS", r'class'),
    (3, "MAIN", r'main'),
        (5, "IF", r'if'),
        (6, "ELSE", r'else'),
        (7, "WHILE", r'while'),
        (8, "FOR", r'for'),
        (9, "RETURN", r'return'),
        (10, "BREAK", r'break'),
        (11, "CONTINUE", r'continue'),
    (4, "ESTRUCTURA CONTROL", r"if|else|while|for"),
    (12, "NEW", r'new'),
    (13, "PRINT", r'print'),
    (14, "READ", r'read'),
        (22, "INT", r'int'),
        (23, "DOUBLE", r'double'),
        (24, "STRING", r'string'),
        (25, "BOOLEAN", r'boolean'),
        (26, "CHAR", r'char'),
        (27, "VOID", r'void'),
    (21, "TIPO DATO", r'int|double|string|boolean|char'),
    (1, "PALABRA RESERVADA", r'\b(class|public|private|static|main|if|else|while|for|return|new|print|read|int|double|string|boolean|char|void|break|continue)'),
    
    # Identificadores y literales (31-40)
    (31, "IDENTIFICADOR", r'[a-zA-Z_][a-zA-Z0-9_]*'),
        (33, "REAL", r'\-?\d+?\.\d+'),
        (34, "ENTERO", r'\-?\d+'),
        (35, "CADENA", r'"[^"]*"'),
        (36, "CARACTER", r"'(\\.|[^'\\])'"),
        (37, "TRUE", r'true'),
        (38, "FALSE", r'false'),
    (32, "DATOS", r'((\-?\d+\.\d+)|(\-?\d+)|("[^"]*")|(\'(\\.|[^\'\\])\'))|true|false'),
    
    
    # Comentarios (41-50)
    (41, "COMENTARIO LINEA", r'//[^\n]*\n'),
    (42, "COMENTARIO BLOQUE", r'/\*[\s\S]*?\*/'),
    # (42, "COMENTARIO BLOQUE", r'/\*[\s\S]*?\*/'),
    
    # Operadores aritméticos (51-60)
        (52, "OP SUMA", r'\+'),
        (53, "OP RESTA", r'-'),
        (54, "OP MULTIPLICACION", r'\*'),
        (55, "OP DIVISION", r'/'),
    (51, "OP ARITMETICO", r'\+|-|\*|/'),
    
    # Operadores lógicos (61-70)
    (62, "OP AND", r'&&'),
    (63, "OP OR", r'\|\|'),
    (64, "OP NOT", r'!'),
    (61, "OP LOGICO", r'&&|\|\||!'),

    # Operadores relacionales (71-80)
    (72, "OP IGUAL", r'=='),
    (73, "OP DISTINTO", r'!='),
    (74, "OP MAYOR IGUAL", r'>='),
    (75, "OP MENOR IGUAL", r'<='),
    (76, "OP MAYOR", r'>'),
    (77, "OP MENOR", r'<'),
    (71, "OP RELACIONAL", r'(==|!=|>|>=|<|<=)'),
    
    # Operador de asignación (80)
    (80, "OP ASIGNACION", r'='),

    # Símbolos de agrupación (81-90)
        (82, "PARENTESIS IZQ", r"\("),
        (83, "PARENTESIS DER", r"\)"),
        (84, "CORCHETE IZQ", r'\['),
        (85, "CORCHETE DER", r'\]'),
        (86, "LLAVE IZQ", r'\{'),
        (87, "LLAVE DER", r'\}'),
    (81, "SIMBOLO AGRUPACION", r'\(|\)|\[|\]|\{|\}'),
    
    # Símbolos especiales (91-100)
        (92, "COMA", r','),
        (93, "PUNTO", r'\.'),
        (94, "PUNTO Y COMA", r';'),
    (91, "SIMBOLO ESPECIAL", r'\,|;|\.'),
    
    # Espacios
    (101, "ESPACIO", r'\s+'),
    (102, "SALTO LINEA", r'\n')
]