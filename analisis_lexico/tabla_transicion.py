tabla_transicion = {
    "IDENTIFICADOR": {
        "INICIO": "q0",
        "q0": {
            "LETRA": "q1",
            "_": "q1"
        },
        "q1": {
            "LETRA": "q1",
            "DIGITO": "q1",
            "_": "q1"
        },
        "FIN": ["q1"]
    },
    "ENTERO": {
        "INICIO": "q0",
        "q0": {
            "OP MENOS": "q1",
            "DIGITO": "q2"
        },
        "q1": {
            "DIGITO": "q2"
        },
        "q2": {
            "DIGITO": "q2"
        },
        "FIN": ["q2"]
    },
    "REAL": {
        "INICIO": "q0",
        "q0": {
            "OP MENOS": "q1",
            "DIGITO": "q2",
            "PUNTO": "q3"
        },
        "q1": {
            "DIGITO": "q2",
            "PUNTO": "q3"
        },
        "q2": {
            "DIGITO": "q2",
            "PUNTO": "q3"
        },
        "q3": {
            "DIGITO": "q4"
        },
        "q4": {
            "DIGITO": "q4"
        },
        "FIN": ["q4"]
    },
    "CADENA": {
        "INICIO": "q0",
        "q0": {
            "COMILLA DOBLE": "q1"
        },
        "q1": {
            "LETRA": "q1",
            "DIGITO": "q1",
            "_": "q1",
            "'": "q1",
            "OP MAS": "q1",
            "OP MENOS": "q1",
            "OP POR": "q1",
            "SLASH": "q1",
            "OP MENOR": "q1",
            "OP MAYOR": "q1",
            "OP AMPER": "q1",
            "OP PIPE": "q1",
            "OP NOT": "q1",
            "OP IGUAL": "q1",
            "PARENTESIS IZQ": "q1",
            "PARENTESIS DER": "q1",
            "CORCHETE IZQ": "q1",
            "CORCHETE DER": "q1",
            "LLAVE IZQ": "q1",
            "LLAVE DER": "q1",
            "COMA": "q1",
            "PUNTO": "q1",
            "PUNTO Y COMA": "q1",
            "SALTO LINEA": "q1",
            "ESPACIO": "q1",
            "DESCONOCIDO": "q1",
            "COMILLA_SIMPLE": "q1",
            "COMILLA DOBLE": "q2"
        },
        "q2": {},
        "FIN": ["q2"]
    },
    "CARACTER": {
        "INICIO": "q0",
        "q0": {
            "COMILLA SIMPLE": "q1"
        },
        "q1": {
            "LETRA": "q2",
            "DIGITO": "q2",
            "_": "q2",
            "OP MAS": "q2",
            "OP MENOS": "q2",
            "OP POR": "q2",
            "SLASH": "q2",
            "OP MENOR": "q2",
            "OP MAYOR": "q2",
            "OP AMPER": "q2",
            "OP PIPE": "q2",
            "OP NOT": "q2",
            "OP IGUAL": "q2",
            "PARENTESIS IZQ": "q2",
            "PARENTESIS DER": "q2",
            "CORCHETE IZQ": "q2",
            "CORCHETE DER": "q2",
            "LLAVE IZQ": "q2",
            "LLAVE DER": "q2",
            "COMA": "q2",
            "PUNTO": "q2",
            "PUNTO Y COMA": "q2",
            "SALTO LINEA": "q2",
            "ESPACIO": "q2",
            "DESCONOCIDO": "q2",
            "COMILLA SIMPLE": "q2"
        },
        "q2": {
            "COMILLA SIMPLE": "q3"
        },
        "q3": {},
        "FIN": ["q3"]
    },
    "COMENTARIO LINEA": {
        "INICIO": "q0",
        "q0": {
            "SLASH": "q1"
        },
        "q1": {
            "SLASH": "q2"
        },
        "q2": {
            "LETRA": "q2",
            "DIGITO": "q2",
            "_": "q2",
            "OP MAS": "q2",
            "OP MENOS": "q2",
            "OP POR": "q2",
            "SLASH": "q2",
            "OP MENOR": "q2",
            "OP MAYOR": "q2",
            "OP AMPER": "q2",
            "OP PIPE": "q2",
            "OP NOT": "q2",
            "OP IGUAL": "q2",
            "PARENTESIS IZQ": "q2",
            "PARENTESIS DER": "q2",
            "CORCHETE IZQ": "q2",
            "CORCHETE DER": "q2",
            "LLAVE IZQ": "q2",
            "LLAVE DER": "q2",
            "COMA": "q2",
            "PUNTO": "q2",
            "PUNTO Y COMA": "q2",
            "ESPACIO": "q2",
            "DESCONOCIDO": "q2",
            "COMILLA SIMPLE": "q2",
            "COMILLA DOBLE": "q2",
            "SALTO LINEA": "q3",
            "EOF": "q3"
        },
        "q3": {},
        "FIN": ["q3"]
    },
    "COMENTARIO BLOQUE": {
        "INICIO": "q0",
        "q0": {
            "SLASH": "q1"
        },
        "q1": {
            "OP POR": "q2"
        },
        "q2": {
            "LETRA": "q2",
            "DIGITO": "q2",
            "_": "q2",
            "'": "q2",
            "OP MAS": "q2",
            "OP MENOS": "q2",
            "SLASH": "q2",
            "OP MENOR": "q2",
            "OP MAYOR": "q2",
            "OP AMPER": "q2",
            "OP PIPE": "q2",
            "OP NOT": "q2",
            "OP IGUAL": "q2",
            "PARENTESIS IZQ": "q2",
            "PARENTESIS DER": "q2",
            "CORCHETE IZQ": "q2",
            "CORCHETE DER": "q2",
            "LLAVE IZQ": "q2",
            "LLAVE DER": "q2",
            "COMA": "q2",
            "PUNTO": "q2",
            "PUNTO Y COMA": "q2",
            "SALTO LINEA": "q2",
            "ESPACIO": "q2",
            "DESCONOCIDO": "q2",
            "COMILLA SIMPLE": "q2",
            "COMILLA DOBLE": "q2",
            "OP POR": "q3"
        },
        "q3": {
            "LETRA": "q2",
            "DIGITO": "q2",
            "_": "q2",
            "'": "q2",
            "OP MAS": "q2",
            "OP MENOS": "q2",
            "OP MENOR": "q2",
            "OP MAYOR": "q2",
            "OP AMPER": "q2",
            "OP PIPE": "q2",
            "OP NOT": "q2",
            "OP IGUAL": "q2",
            "PARENTESIS IZQ": "q2",
            "PARENTESIS DER": "q2",
            "CORCHETE IZQ": "q2",
            "CORCHETE DER": "q2",
            "LLAVE IZQ": "q2",
            "LLAVE DER": "q2",
            "COMA": "q2",
            "PUNTO": "q2",
            "PUNTO Y COMA": "q2",
            "SALTO LINEA": "q2",
            "ESPACIO": "q2",
            "DESCONOCIDO": "q2",
            "COMILLA SIMPLE": "q2",
            "COMILLA DOBLE": "q2",
            "OP POR": "q3",
            "SLASH": "q4"
        },
        "q4": {},
        "FIN": ["q4"]
    }
}