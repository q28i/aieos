# aieos.py
"""
Primary entrypoint wrapper for the AIEOS Command Line Interface.
"""
import sys
from doc_system.cli import AIEOS_CLI

def main():
    cli = AIEOS_CLI()
    success = cli.execute(sys.argv[1:])
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
