#!/usr/bin/env python
"""
Implements a simple Logical Expression Evaluator. Prints 
the Truth Table for the given expression.

	Originally written by Osmar D. Gómez A 
	(ogomez384@e.uneg.edu; 	tutor.the.code@gmail.com)

	Grammar:

	<eval> ::= ";"
	       |   "exit"
	       |   <prop>
	       |   <eval> <prop>
			
	<prop> ::= <term>
	       |   <prop>  "->"  <term>
	       |   <prop> "<->"  <term>
	       |   <prop> "<~>"  <term>

	<term> ::= <atom>
	       |   <term> "&" <atom>
	       |   <term> "|" <atom>
	       |   <term> "!" <atom>

	<atom> ::= <id>
	       | "~" <atom>
	       | "(" <prop> ")"
	       | "[" <prop> "]"
	       | "{" <prop> "}"

	<id> ::= [a-zA-Z]{1,1}

#-----------------------------------------------------------

EXAMPLES (copied directly from output), '>' is the prompt.

> (a & ~r );
a  r  ~r  (a&~r)
================
V  V   F     F
V  F   V     V
F  V   F     F
F  F   V     F
================
(a&~r) = contingent

You can use comments:

> ~(a & b) <-> (~a | ~b); ## De Morgan´s
a  b  (a&b)  ~(a&b)  ~a  ~b  (~a|~b)  ~(a&b)<->(~a|~b)
======================================================
V  V    V       F     F   F     F             V
V  F    F       V     F   V     V             V
F  V    F       V     V   F     V             V
F  F    F       V     V   V     V             V
======================================================
~(a&b)<->(~a|~b) = tautology


> (a ! b) <-> ~(a | b); ## '!' is Joint Negation (↓)
a  b  (a!b)  (a|b)  ~(a|b)  (a!b)<->~(a|b)
==========================================
V  V    F      V       F           V
V  F    F      V       F           V
F  V    F      V       F           V
F  F    V      F       V           V
==========================================
(a!b)<->~(a|b) = tautology


> [(a & b) -> c] <-> [a -> (b -> c)];
a  b  c  (a&b)  [(a&b)->c]  (b->c)  [a->(b->c)]  [(a&b)->c]<->[a->(b->c)]
=========================================================================
V  V  V    V         V         V         V                   V
V  V  F    V         F         F         F                   V
V  F  V    F         V         V         V                   V
V  F  F    F         V         V         V                   V
F  V  V    F         V         V         V                   V
F  V  F    F         V         F         V                   V
F  F  V    F         V         V         V                   V
F  F  F    F         V         V         V                   V
=========================================================================
[(a&b)->c]<->[a->(b->c)] = tautology


> {(a & b) <-> [(p | ~q) -> s]};
a  b  p  q  s  (a&b)  ~q  (p|~q)  [(p|~q)->s]  {(a&b)<->[(p|~q)->s]
===================================================================
V  V  V  V  V    V     F     V         V                 V
V  V  V  V  F    V     F     V         F                 F
V  V  V  F  V    V     V     V         V                 V
V  V  V  F  F    V     V     V         F                 F
V  V  F  V  V    V     F     F         V                 V
V  V  F  V  F    V     F     F         V                 V
V  V  F  F  V    V     V     V         V                 V
V  V  F  F  F    V     V     V         F                 F
V  F  V  V  V    F     F     V         V                 F
V  F  V  V  F    F     F     V         F                 V
V  F  V  F  V    F     V     V         V                 F
V  F  V  F  F    F     V     V         F                 V
V  F  F  V  V    F     F     F         V                 F
V  F  F  V  F    F     F     F         V                 F
V  F  F  F  V    F     V     V         V                 F
V  F  F  F  F    F     V     V         F                 V
F  V  V  V  V    F     F     V         V                 F
F  V  V  V  F    F     F     V         F                 V
F  V  V  F  V    F     V     V         V                 F
F  V  V  F  F    F     V     V         F                 V
F  V  F  V  V    F     F     F         V                 F
F  V  F  V  F    F     F     F         V                 F
F  V  F  F  V    F     V     V         V                 F
F  V  F  F  F    F     V     V         F                 V
F  F  V  V  V    F     F     V         V                 F
F  F  V  V  F    F     F     V         F                 V
F  F  V  F  V    F     V     V         V                 F
F  F  V  F  F    F     V     V         F                 V
F  F  F  V  V    F     F     F         V                 F
F  F  F  V  F    F     F     F         V                 F
F  F  F  F  V    F     V     V         V                 F
F  F  F  F  F    F     V     V         F                 V
===================================================================
{(a&b)<->[(p|~q)->s]} = contingent


> (p & ~p);
p  ~p  (p&~p)
=============
V   F     F
F   V     F
=============
(p&~p) = contradiction


ERRORS:

> something & p;  ## BAD
BadIdentifierError: name 'something' too long, should be one character

> s & p; ## GOOD
s  p  s&p
=========
V  V   V
V  F   F
F  V   F
F  F   F
=========
s&p = contingent

> {(p -> q) & r; ## BAD
NotExpectedError: '}' expected

> {(p -> q) & r}; ## GOOD
p  q  r  (p->q)  {(p->q)&r}
===========================
V  V  V     V         V
V  V  F     V         F
V  F  V     F         F
V  F  F     F         F
F  V  V     V         V
F  V  F     V         F
F  F  V     V         V
F  F  F     V         F
===========================
{(p->q)&r} = contingent


> p -> ;  ## BAD
NotExpectedError: an atom expected

> p -> q; ## GOOD
p  q  p->q
==========
V  V    V
V  F    F
F  V    V
F  F    V
==========
p->q = contingent

"""

from TableParse import *
from TokenStream import (EXIT, END, EvaluatorError, 
	                     Stream, SEEK_SET)

class TruthTable:
	""
	def __init__(self, ts: TokenStream):
		self.vartable = {}		
		self.sb = Stream()     # reuse expression
		for t in ts:
			self.sb.write(ident := f"{t:v}")
			if t.kind is IDENTIFIER: 
				self.vartable[ident] = None

		# setup variable initial values
		if not self.vartable:
			raise EvaluatorError("must enter at least one variable")
		self.nrows = setup_variables(self.vartable)
		


	def print(self):		

		contxt = self.vartable
		expr   = self.sb.getvalue()
		## recreate token stream and evaluate
		prop(TokenStream(f"{expr};"), contxt)
		
		self.sb.truncate(SEEK_SET)
		self.sb.seek(SEEK_SET)
		file = self.sb

		# print table header
		print(*contxt, sep='  ', file=file)
		print(f"{(sepline := '=' * len('  '.join(contxt)))}", file=file)

		# print table/values
		table  = contxt.items()
		depth = self.nrows
		fmt   = lambda lable, value: \
					f"{'V' if value else 'F':^{1 + len(lable)}} "

		print(*("".join(r) for r in ([fmt(l, v[i]) for l, v in table] 
			for i in range(depth))), sep='\n', file=file)	

		# Print table result		
		print("{}\n{} = {}\n".format(sepline, expr,
			   'tautology'  if all(rc := contxt[expr]) else 
			   'contingent' if any(rc) else 'contradiction'), file=file)

		return file.getvalue()



def main():

	ts = TokenStream() # read from stdin
	print("> ", end="", flush=True)
	while (tok := ts.next()).kind is not EXIT:
 		try:
	 		ts.putback(tok)
	 		print(f"{TruthTable(ts).print()}")

 		except (EvaluatorError, Exception) as e:
	 		print(f"{type(e).__name__}: {e}")
	 		if isinstance(e, ValueError):
	 			while ts.next().kind is not END: "clean up buffer"
	 		ts = TokenStream()

	 	print("> ", end="", flush=True)


if __name__ == '__main__':
	main()

	
	

 


	
	

