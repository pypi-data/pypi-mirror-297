import sys
from . import quote

def main():
    if len(sys.argv) < 3:
        print("Usage: eqsor-cli <oms log filename> <quote csv filename> [<envID>]")
        sys.exit(1)

    input_log = sys.argv[1]
    output_csv = sys.argv[2]
    env_id = sys.argv[3]

    result = quote(input_log, output_csv, env_id)
    if result == 0:
        print("Success quote csv generated")
    else:
        print("Error quote csv not generated")
