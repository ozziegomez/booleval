

from Utils import *
from TokenStream import (TokenStream, 
	                     IDENTIFIER, NOT, 
	                     connective, separator_pairs,
                         BadIdentifierError, NotExpectedError)


def prop(ts: TokenStream, context: dict) -> str:

	a = term(ts, context)
	while is_prop(k := (tok := ts.next()).kind):
		b = term(ts, context)		
		args = zip(context[a], context[b])
		a = F"{a}{tok:v}{b}"
		context[a] = connective[k](args) 
	else:
		ts.putback(tok)
	return a

def term(ts: TokenStream, context: dict) -> str:
	a = atom(ts, context) 
	while is_term(k := (tok := ts.next()).kind):
		b = atom(ts, context)
		args = zip(context[a], context[b])
		a = F"{a}{tok:v}{b}"
		context[a] = connective[k](args) 
	else:
		ts.putback(tok)
	return a 

def atom(ts: TokenStream, context) -> str:
	if (k := (tok := ts.next()).kind) is NOT:
		a = atom(ts, context)
		context[F"{k:v}{a}"] = connective[NOT](context[a])
		return F"{k:v}{a}"

	if k is IDENTIFIER:
		if 1 != len(tok.value): 
			raise BadIdentifierError(
			f"name '{tok:v}' too long, should be one character") 
		return f'{tok:v}'

	if is_left_pair(left := k):
	    a = prop(ts, context) 
	    if ts.next().kind is not (right := separator_pairs[left]):
	    	raise NotExpectedError(F"'{right:v}' expected")
	    # update a with proper separator
	    a, old = F"{left:v}{a}{right:v}", a
	    context[a] = context.pop(old)
	    return a

	raise NotExpectedError("an atom expected")