
from pathlib import Path
import sys
import webbrowser

curdir = Path(__file__).parent
sys.path += [f"{curdir!s}"]

try:
	import truthtable
	
	match "".join(sys.argv[1:2]).lower():
		case "help": 
			webbrowser.open(f'{curdir / "README.html"}')
		case _:
			"IGNORE"				

	truthtable.main()
	
except Exception as e:
	print(f"Oops: {e}")

	