grammar AutoQcm;

document 
  : (element)+? EOF
  ;

/* Rules of elements allowed within a document */
element
  : headline
  | directive
  | comment
  | listItemBullet
  | listItemEnumerated
  | tabular
  | paragraph
  | empty_line
  ;

/* Headline Rule */
headline
    :  LB level indentation points? (title = rawLineContent) isQuestion =':question:'?
    ;

level
  : (STAR)+
  ;

points
  : O_S_BRACKET NUMBERS C_S_BRACKET WS+
  ;

directive
  :  LB indentation? DIRECTIVE name = keyword  COLON WS* value = rawLineContent
  ;

/* Comment Rule */
comment
  :  LB indentation? COMMENT (content = commentLineNoBreak)
  ;
commentLineNoBreak
  :  commentLineAtoms
  ;
commentLineAtoms
  :  ~(LB)+
  ;



listItemBullet
  :  bulletCrossLine
  |  bulletSimple
  |  LB indentation? special=(MINUS | PLUS)
  ;
bulletCrossLine
  :  LB WS* bullet checkBox? WS* (paragraph+)? 
  ;
bulletSimple 
  :  LB WS* bullet checkBox? WS+ paragraphNoBreak paragraph*?
  ;

bullet
  :  MINUS 
  |  PLUS
  ;
checkBox
  :  WS O_S_BRACKET isChecked C_S_BRACKET
  ;
isChecked
  :  (WS | 'x' | 'X')
  ;
listItemEnumerated
  :  LB WS* enumerated=lineSpecial WS+ paragraphNoBreak paragraph*
  ;  

/* Tabular rule */
tabular
  : tabularRow+
  ;

tabularRow
  : LB indentation? PLUS MINUS tabularCellHline tabularMixinCell*?
  | LB indentation? PIPE tabularMixinCell+?
  ;

tabularMixinCell
  : tabularCellHline
  | tabularCell
  ;

tabularCellHline
  : content+=MINUS+? PLUS
  ;

tabularCell
  : content = tabularCellContent (PIPE | PLUS | LB)
  ;
tabularCellContent
  : ~(PIPE | PLUS | MINUS) span span*?
  ;


paragraph
  :  line+?
  ;

paragraphNoBreak
  :  lineNoBreak
  ;

lineNoBreak
  :  indentation? span+?
  ;
  
line
  :  LB indentation? span+?
  ;
  

lineSpecial
  :  indentation? O_LIST_BULLET
  ;

spanLineStartNoEmphasis
  :  hyperlink
  |  latexEntity
  |  latexFragment
  |  emphCode
  |  emphVerbatim
  |  emphasis
  |  textLineStart
  ;

// Non greedy operator important for both
textLineStart
  :  lineStart_fragment+? text_fragment*?
  ;
  
lineStart_fragment
  :  BEGIN
  |  END
  |  NUMBERS
  |  ALPHABET
  |  WS
  |  O_S_BRACKET
  |  C_S_BRACKET
  |  O_ANGLE
  |  C_ANGLE
  |  O_PAREN
  |  C_PAREN
  |  QUOTE
  |  COLON
  |  COMMA
//  |  EQUAL
//  |  TILDE
//  |  STAR
//  |  UNDERSCORE
//  |  SLASH
//  |  PLUS
  |  DOT
  |  ANY
  ;
 
// Non greedy operator important for both
text
  :  lineStart_fragment+? text_fragment*?
  ;

textStart
  :  lineStart_fragment
  |  text_fragment_start text_fragment_start+?
  //|  WS
  ;

span
  :  hyperlink
  |  latexEntity
  |  latexFragment
  |  emphCode
  |  emphVerbatim
  |  emphasis
  |  text
  ;

text_fragment_start
  :  NUMBERS
  |  ALPHABET
  |  WS
  |  O_S_BRACKET
  |  C_S_BRACKET
  |  O_ANGLE
  |  C_ANGLE
  |  O_PAREN
  |  C_PAREN
  |  QUOTE
  |  COLON
  |  COMMA
  |  EQUAL
  |  TILDE
  |  STAR
  |  UNDERSCORE
  |  SLASH
  |  MINUS
  |  DOT
  |  ANY
  ;

text_fragment
  :  text_fragment_start
  |  COMMENT
  |  DIRECTIVE
//  |  H_LEVEL
  |  DOT
  ;

hyperlink
  :  O_S_BRACKET O_S_BRACKET url C_S_BRACKET C_S_BRACKET
  ;
 
url
  :  ~( LB | O_S_BRACKET | C_S_BRACKET  )+?
  ;
  
latexEntity
  : BACK_SLASH name=ALPHABET brackets?
  ;
brackets
  : O_S_BRACKET content+=~( O_BRACKET | C_BRACKET | O_S_BRACKET | C_S_BRACKET | LB) C_S_BRACKET
  | O_BRACKET content+=~( O_BRACKET | C_BRACKET | LB) C_BRACKET
  ;
latexFragment
  : ESC_O_S_BRACKET content+=~( ESC_C_S_BRACKET )* ESC_C_S_BRACKET
  | ESC_O_PAREN content+=~( ESC_C_PAREN )* ESC_C_PAREN
  | DOLLAR content+=~( DOLLAR )* DOLLAR
  ;

emphCode
  : TILDE ~( TILDE | WS ) ~( TILDE )*? TILDE
  ;

emphVerbatim
  : EQUAL ~( EQUAL | WS ) ~( EQUAL )*? EQUAL
  ;

emphasis 
  : UNDERSCORE ( emphasis | text )*? UNDERSCORE
  | SLASH ( emphasis | text )*? SLASH
  | STAR ( emphasis | text )*? STAR
  | PLUS ( emphasis | text )*? PLUS
  ;

keyword
  : (ALPHABET | UNDERSCORE)+
  ;
indentation
  : WS+
  ;
rawLineContent
  : ~(LB)*?
  ;

empty_line
  : LB WS*
  ;







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
SLASH
  : '/'
  ;
EQUAL
  : '='
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
