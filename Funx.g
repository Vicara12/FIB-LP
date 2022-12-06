grammar Funx;

root : (varassig | expr)* ;

varassig : VARNAME '<-' expr ;

expr : '(' expr ')'                 # Parentheses
    | <assoc=right> expr POW expr   # Power
    | expr (MULT | DIV | MOD) expr  # MultDivMod
    | expr (PLUS | MINUS) expr      # PlusMinus
    | NUM                           # Number
    | VARNAME                       # Variable
    ;

NUM : [0-9]+ ;
PLUS : '+' ;
MINUS : '-' ;
MULT : '*' ;
DIV : '/' ;
POW : '^' ;
MOD : '%' ;
VARNAME : [a-z] [a-zA-Z0-9]* ;
COMMENT : '#' (~[\n])* '\n' -> skip;
WS : [ \t\n]+ -> skip ;
