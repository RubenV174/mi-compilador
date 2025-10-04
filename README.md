# Compilador

Este proyecto es la implementación del frontend de un compilador para un lenguaje de alto nivel similar a Java/C#. El compilador está escrito completamente en Python y cubre las tres fases fundamentales del análisis de código fuente: análisis léxico, sintáctico y semántico.

## Características
**Analizador Léxico (Lexer):** 
Convierte el código fuente en una lista de tokens mediante expresiones regulares.
<br/>
**Analizador Sintáctico: (Parser):**
Se revisa que el codigo este bien estructurado. Muestra el resultado mediante un *AST* (Árbol Sintáctico)
<br/>
**Analizador Sintáctico: (Semantic):**
Se revisa la coherencia del codigo y la compatibilidad del código, devuelve una lista de variables. **NOTA: EN EL ANALIZADOR SINTÁCTICO SE INCLUYE LA SEMANTICA POR LO QUE EL SEMÁNTICO NO CORRERA NADA**

## Estructura
```bash
|-analisis_lexico/
|----|-lexer.py             # Analizador Léxico
|----|-tabla_transicion.py  # Tabla de donde se obtendran algunos tokens
|----|-tokens.py            # Clase tokens de donde se extrae la estructura de los tokens
|----|-expr_reg.py          # Expresiones Regulares de las cuales se definen los tokens 
|-Main.py
|-code.txt              # Codigo que se usará para probar el compilador
```

## Ejecución
1. Clonar el repositorio
```bash
git clone https://github/RubenV174/mi-compilador.git
cd mi-compilador
```
2. Ejecutar el compilador
```bash
python -m Main.py
```
3. Si se requieren hacer pruebas individuales:
```bash
python -m analisis_lexico\lexer.py
```