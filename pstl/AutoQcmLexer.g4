lexer grammar AutoQcmLexer;

fragment A : [aA]; // match either an 'a' or 'A'
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];

BEGIN
  : B E G I N
  ;

END
  : E N D
  ;
O_LIST_BULLET
  : NUMBERS DOT 
  ;

DIRECTIVE
  : HASH PLUS
  ;

COMMENT
  : HASH WS
  ;
D_DOLLAR
  : DOLLAR 
  ;
H_LEVEL
	: STAR+
	;

ALPHABET
  : [A-Za-z]+
  ;

  
NUMBERS
  : [0-9]+
  ;
DOLLAR
  : '$'
  ;

DOT
  : '.'
  ;
ESC_O_S_BRACKET
  : BACK_SLASH O_S_BRACKET
  ;
ESC_C_S_BRACKET
  : BACK_SLASH C_S_BRACKET
  ;  
ESC_O_BRACKET
  : BACK_SLASH O_BRACKET
  ;
ESC_C_BRACKET
  : BACK_SLASH C_BRACKET
  ;  
ESC_O_PAREN
  : BACK_SLASH O_PAREN
  ;
ESC_C_PAREN
  : BACK_SLASH C_PAREN
  ; 
O_S_BRACKET
  : '['
  ;

C_S_BRACKET
  : ']'
  ;
O_BRACKET
  : '{'
  ;

C_BRACKET
  : '}'
  ;
O_ANGLE
  : '<'
  ;

C_ANGLE
  : '>'
  ;
O_PAREN
  : '('
  ;

C_PAREN
  : ')'
  ;
HASH
  : '#'
  ;

UNDERSCORE
  : '_'
  ;
COLON
  : ':'
  ;
COMMA
  : ','
  ;
TILDE
  : '~'
  ;
BACK_SLASH
  : '\\'
  ;
QUOTE
  : '\''
  ;
STAR
  : '*'
  ;

MINUS
  : '-'
  ;
PLUS
  : '+'
  ;

PIPE
  : '|'
  ;

WS
  :  ' ' 
  |  '\t'
  ;

LB
  :  '\r'? '\n'
  ;

ANY
  :  .
  ;
