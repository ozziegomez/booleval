#!/usr/bin/env python
"""
Implements a simple Logical Expression Evaluator. 

Prints the Truth Table for the given expression.

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

"""

from TableParse import *
from TokenStream import (EXIT, END, EvaluatorError, 
	                     Stream, SEEK_SET, ts)

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
		


	def __repr__(self):		

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

	print("> ", end="", flush=True)
	while (tok := ts.next()).kind is not EXIT:
 		try:
	 		ts.putback(tok)
	 		print(f"{TruthTable(ts)}")

 		except (EvaluatorError, Exception) as e:
	 		print(f"{type(e).__name__}: {e}")
	 		if isinstance(e, ValueError):
	 			while ts.next().kind is not END: "clean up buffer"
	 		ts = TokenStream()

	 	print("> ", end="", flush=True)


if __name__ == '__main__':
	main()

	
	

 


	
	

