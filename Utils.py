
from TokenStream import (NOT, IMPLIES, IFF, SHEFFER, AND, 
	                     OR, JOINTNEG, LPAREN, LBRACE, LBRACKET)

__all__ = ["setup_variables",
           "is_prop", 
           "is_term", 
           "is_valid",
           "is_left_pair"]

## Utility
def setup_variables(names):
	depth = 2 ** len(names)
	for i, n in enumerate(names):
		names[n] = tuple(x for x in (1, 0) * 2**i 
			               for _ in range(depth//2**(1+i)))
	return depth

def is_prop(k): 
	return any(k is x for x in (IMPLIES, IFF, SHEFFER))

def is_term(k): 
	return any(k is x for x in (AND, OR, JOINTNEG))

def is_left_pair(k):
	return any(k is x for x in (LPAREN, LBRACKET, LBRACE))

def is_valid(k):
	return any(k is NOT, is_prop(k), is_term(k))
