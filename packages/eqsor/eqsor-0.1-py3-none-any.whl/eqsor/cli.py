import sys
from . import quote

def main():
    if len(sys.argv) < 3:
        print("Usage: eqsor-cli <oms log filename> <quote csv filename> [<envID>]")
        sys.exit(1)

    input1 = sys.argv[1]
    input2 = sys.argv[2]
    input3 = sys.argv[3] if len(sys.argv) > 3 else None

    result = quote(input1, input2, input3)
    if result == 0:
        print("Success quote csv generated")
    else:
        print("Error quote csv not generated")
