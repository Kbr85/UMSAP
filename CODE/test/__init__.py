import sys
from pathlib import Path

umsapPath = Path(__file__).parent.parent
umsapPath = umsapPath / 'umsap'

sys.path.append(str(umsapPath))

print(sys.path)