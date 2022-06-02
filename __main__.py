
from pathlib import Path
import sys

curdir = Path(__file__).parent
sys.path += [f"{curdir!s}"]

try:
	import truthtable
	from itertools import takewhile, dropwhile

	doc = truthtable.__doc__
	pred = lambda l: not l.startswith("#-")

	if (op := "".join(sys.argv[1:2]).lower()) == "about":
		for line in takewhile(pred,	(_ for _ in doc.splitlines())):
			print(line)
	elif op == "examples":
		for line in dropwhile(pred, (_ for _ in doc.splitlines())):
			print(line)
	elif op == "help": 
		with (curdir / 'README.txt').open() as fh: 
			for line in fh: print(line)
	truthtable.main()
except Exception as e:
	print(f"Oops: {e}")

	