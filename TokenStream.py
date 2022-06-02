__author__ = "Osmar Gómez A. <tutor.the.code@gmail.com>"

from enum import Enum
import sys
from io import (TextIOWrapper, 
	            SEEK_SET,
	            StringIO as Stream)

class Lexeme(Enum):
	"Lexical units"
	Unknown    = "?"
	Identifier = "identifier"
	Number     = "number"
	Not        = "~"
	And        = "&"
	Or         = "|"
	JointNeg   = "!"
	Implies    = "->"
	Iff        = "<->"
	Sheffer    = "<~>"
	LParen     = "("
	RParen     = ")"
	LBracket   = "["
	RBracket   = "]"
	LBrace     = "{"
	RBrace     = "}"
	End        = ";"
	Exit       = "exit"

	def __format__(self, spec):
		if spec == 'v': return self.value 
		if spec == 'n': return self.name 
		return super().__format__(spec)

for m in Lexeme: 
	exec(f"{m.name.upper()} = {m}")

## match each separator
separator_pairs = {
	LPAREN: RPAREN, 
	LBRACKET: RBRACKET, 
	LBRACE: RBRACE
}

connective = {
	NOT:      lambda d: tuple(not x for x in d),
	AND:      lambda d: tuple(x and y for x, y in d),
	OR:       lambda d: tuple(x or y for x, y in d),
	JOINTNEG: lambda d: tuple(not(x or y) for x, y in d),
	IMPLIES:  lambda d: tuple(not x or y for x, y in d),
	IFF:      lambda d: tuple(not(x or y) or (x and y) for x, y in d),
	SHEFFER:  lambda d: tuple((x or y) and not(x and y)
		for x, y in d)
}


class EvaluatorError(Exception):
	"Base Exception for the Evaluator"
class BadNumberError(EvaluatorError):
	"Raised by CharStream#nextn"
class FullBufferError(EvaluatorError):
	"Raised by CharStream#putback and TokenStream#putback"
class NotExpectedError(EvaluatorError):
	"Raised when we get a bad token"
class BadIdentifierError(EvaluatorError):
	"Names of variables should be one character long"

	
class Token:
	
	def __init__(self, kind: Lexeme, value: str) -> None:
		self.kind = kind
		self.value = value 

	def __repr__(self):
		return (F"{self.__class__.__name__}("
			F"{self:k}, '{self:v}')")

	def __format__(self, spec):
		if spec == 'k': return f"{self.kind:n}".upper()
		if spec == 'v': return self.value 
		return super().__format__(spec)

	__slots__ = ('kind', 'value')

## Represents a stream of characters from some input source
## default source is sys.stdin. This class for the use of
## TokenStream.
class _CharStream:
	def __init__(self, src: TextIOWrapper):
		self.src = src
		self.cached = None

	def isfull(self):
		return self.cached is not None

	def ignore_spaces(self, c):
		while c.isspace(): c = self.get()
		return c

	def ignore_comments(self, c):
		while c == '#':
			c = self.ignore_spaces(self.ignore_until(c, '\n'))
		return c

	def ignore_until(self, c, stop='\n'):
		while c != stop: c = self.get()
		return c

	## returns cached char and set buff to None
	## isfull() should be called first
	def cached_char(self):
		c, self.cached = self.cached, None
		return c

	def putback_char(self, c):
		if self.isfull():
			raise FullBufferError("putback into fullbuffer buffer")
		self.cached = c

	def get(self, n = 1):
		return self.src.read(n)

	## swallows whitespaces and comments
	def getc(self):
		c = self.cached_char() if self.isfull() else self.get()
		return self.ignore_comments(self.ignore_spaces(c))

	def gets(self):
		result = self.getc()		
		while (c := self.get()).isidentifier():
			result += c 
		self.putback_char(c)
		return result 

	def getn(self):
		"""returns the numbers as strings
		"""
		result = self.getc()
		while(c := self.get()).isnumeric():
			result += c 
		self.putback_char(c)
		if ((dots := result.count('.')) == 1 == len(result)
		    or 1 < dots):
			raise BadNumberError(f"bad number")
		return result



class TokenStream(_CharStream):
	"Turn a stream of characters into a stream of tokens"

	def __init__(self, src=None) -> None:
		super().__init__(sys.stdin if src is None 
			                       else Stream(src) if isinstance(src, str)
			                       else src) 
		self.buff  = None

	def fullbuffer(self): 
		return self.buff is not None

	# note: isfull should be called first
	def getbuffer(self):
		tok, self.buff = self.buff, None
		return tok 

	def putback(self, tok: "TokenStream"):
		if self.fullbuffer():
			raise FullBufferError("token putback into a fullbuffer buffer")
		self.buff = tok 

	def next(self):

		## Return cached token if ti's the case
		if self.fullbuffer(): return self.getbuffer()

		## Build a new token
		if (c := self.getc()).isalpha():
			self.putback_char(c)
			if (id := self.gets()) == "exit":
				return Token(EXIT, id)
			return Token(IDENTIFIER, id)
		elif c.isnumeric():
			self.putback_char(c)
			return Token(NUMBER, self.getn())
		elif c == "~":
			return Token(NOT, f"{NOT:v}")
		elif c == '-':
			if (c1 := self.get()) != '>':
				raise ValueError("'->' expected but got '{c}{c1}'")
			return Token(IMPLIES, f"{IMPLIES:v}")
		elif c == '<':
			if ((c1 := f"{c}{self.get(2)}") == f"{IFF:v}" 
				or c1 == f"{SHEFFER:v}"):
				return Token(Lexeme(c1), c1) 
			raise ValueError(f"'<->' or '<~>' expected but got '{c1}'")
		else:
			return Token(Lexeme(c), c)

	def __iter__(self): return self 

	def __next__(self):
		tok = self.next()
		if tok.kind is END: 
			raise StopIteration()
		return tok 

