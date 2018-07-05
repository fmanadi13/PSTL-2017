parser grammar AutoQcmParser;

options {
  tokenVocab=AutoQcmLexer;
}
document 
	: (element)+? EOF
	;

/* Headline Rule */
headline
  	:  LB H_LEVEL indentation (title = rawLineContent)
  	;


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



directive
  :  LB DIRECTIVE name = keyword  COLON WS* value = rawLineContent
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
/*
unorderedList
	: listItemBullet+
	;

orderedList
	: listItemEnumerated+
	;



*/
listItemBullet
  :  bulletCrossLine
  |  bulletSimple
  |  LB indentation? special=(MINUS | PLUS)
  ;
bulletCrossLine
  :  LB WS* bullet WS* (paragraph+)? 
  ;
bulletSimple 
  :  LB WS* bullet WS+ paragraphNoBreak paragraph*
  ;

bullet
  :  MINUS 
  |  PLUS
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
  : content = tabularCellContent (PIPE | PLUS)
  ;
tabularCellContent
	: ~(PIPE | PLUS | MINUS) ~(PIPE | PLUS)*?
	;


paragraph
  :  lines
  ;

paragraphNoBreak
  :  lineNoBreak lines*
  ;

lineNoBreak
  :  indentation? spanLineStartNoEmphasis span*?
  ;
  
lines
  :  linesEmphasis
  |  linesNormal
  ;

linesNormal
  :  lineNormal (linesEmphasis | linesNormal?)
  ;
  
linesEmphasis
  :  lineEmphasis
  |  lineEmphasis lineNoBreak linesNormal??  
  |  lineEmphasis lineNoBreak linesEmphasis
  ;

lineNormal
  :  LB indentation? spanLineStartNoEmphasis+? (span*? spanNoEmphasis+?)?
  ;
  
lineEmphasis
  :  LB indentation? spanLineStartNoEmphasis*? emphasisText
  |  LB indentation? text_fragment+ emphasisText
  ;
 
lineSpecial
  :  indentation? O_LIST_BULLET
  //|  Alphabet Dot
  ;

spanLineStartNoEmphasis
  :  hyperlink
  |  latexEntity
  |  latexFragment
  |  textLineStart
  ;

textLineStart
  :  lineStart_fragment+ text_fragment*
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
  |	 O_PAREN
  |  C_PAREN
  |  QUOTE
  |  COLON
  |  COMMA
  |  DOT
  |  ANY
  ;
 
// Non greedy operator important for both
text
  :  textStart+? text_fragment*?
  ;

textStart
  :  lineStart_fragment
  |  text_fragment_start text_fragment_start+
  |  WS
  ;

spanNoEmphasis
  :  hyperlink
  |  latexEntity
  |  latexFragment
  |  text
  ;

span
  :  emphasisText
  |  spanNoEmphasis
  ;

text_fragment_start
  :  NUMBERS
  |  ALPHABET
  |  WS
  |  C_S_BRACKET
  |  O_ANGLE
  |  C_ANGLE
  |	 O_PAREN
  |  C_PAREN
  |  QUOTE
  |  COLON
  |  COMMA
  |  DOT
  |  ANY
  ;

text_fragment
  :  text_fragment_start
  |  COMMENT
  |  DIRECTIVE
  |  H_LEVEL
  |  DOT
  ;
emphasisText
  :  TILDE+ emphasisNoSpace emphasisAtoms (LB TILDE* emphasisNoSpace emphasisAtoms)* TILDE*
  |  TILDE+ emphasisNoSpace emphasisAtoms TILDE*
  |  TILDE+ emphasisNoSpace emphasisAtoms TILDE+
  ;

emphasisAtoms
  :  emphasisAtom* (TILDE* emphasisAtom)*
  ;

emphasisNoSpace
  :  ~(TILDE | LB | WS)
  ;

emphasisAtom
  :  emph= ~(TILDE | LB) 
  ;


hyperlink
  :  O_S_BRACKET O_S_BRACKET url C_S_BRACKET C_S_BRACKET //(O_S_BRACKET hyperlinkAtom+ C_S_BRACKET)?
  ;
 
url
  :  urlAtom+
  ;
  
urlAtom
  :  ~( LB | O_S_BRACKET | C_S_BRACKET  )
  ;
  
hyperlinkAtom
  :  ~( LB | O_S_BRACKET | C_S_BRACKET )
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
	;

keyword
	: (ALPHABET | UNDERSCORE)+
	;
indentation
	: WS+
	;
rawLineContent
	: ~(LB)*
	;

empty_line
	: LB WS*
	;
