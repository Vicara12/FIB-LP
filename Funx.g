grammar Funx;

root : statement* ;

statement : (while | expr | booleanexpr | varassig) ;


while : WHILE booleanexpr '{' statement* '}' ;

expr : '(' expr ')'                 # Parentheses
    | <assoc=right> expr POW expr   # Power
    | expr (MULT | DIV | MOD) expr  # MultDivMod
    | expr (PLUS | MINUS) expr      # PlusMinus
    | NUM                           # Number
    | VARNAME                       # Variable
    ;

booleanexpr : '(' booleanexpr ')'   # BParentheses
    | NOT booleanexpr               # Not
    | booleanexpr AND booleanexpr   # And
    | booleanexpr OR booleanexpr    # Or
    | expr (GT | GET | LT | LET | EQ | DIF ) expr # Comparison
    | expr                          # ExprToBool
    | TRUE                          # True
    | FALSE                         # False
    | VARNAME                       # BVariable
    ;

varassig : VARNAME '<-' (expr | booleanexpr) ;

NUM : [0-9]+ ;
PLUS : '+' ;
MINUS : '-' ;
MULT : '*' ;
DIV : '/' ;
POW : '^' ;
MOD : '%' ;
NOT : 'not' ;
AND : 'and' ;
OR : 'or' ;
GT : '>' ;
GET : '>=' ;
LT : '<' ;
LET : '<=' ;
EQ : '=' ;
DIF : '!=' ;
WHILE : 'while' ;
TRUE : 'True' ;
FALSE : 'False' ;
VARNAME : [a-z] [a-zA-Z0-9]* ;
COMMENT : '#' (~[\n])* '\n' -> skip;
WS : [ \t\n]+ -> skip ;
