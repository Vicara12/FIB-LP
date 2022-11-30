grammar Funx;

root : expr EOF  ;

expr : '(' expr ')'                 # Parentheses
    | <assoc=right> expr POW expr   # Power
    | expr (MULT | DIV) expr        # MultDiv
    | expr (PLUS | MINUS) expr      # PlusMinus
    | NUM                           # Number
    ;

NUM : [0-9]+ ;
PLUS : '+' ;
MINUS : '-' ;
MULT : '*' ;
DIV : '/' ;
POW : '^' ;
COMMENT : '#' (~[\n])* '\n' -> skip;
WS : [ \t\n]+ -> skip ;
