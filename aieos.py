# aieos.py
"""
Primary entrypoint wrapper for the AIEOS Command Line Interface.
"""
import sys
from doc_system.cli import AIEOS_CLI

def main():
    debug_mode = "--debug" in sys.argv or "-d" in sys.argv
    argv = [arg for arg in sys.argv[1:] if arg not in ["--debug", "-d"]]
    
    from doc_system.cli import AIEOS_CLI
    cli = AIEOS_CLI()
    
    try:
        success = cli.execute(argv)
        sys.exit(0 if success else 1)
    except Exception as e:
        if debug_mode:
            import traceback
            traceback.print_exc()
        else:
            print(f"\033[31mError: Execution failed: {e}\033[0m")
            print("Possible fix: Ensure workspace directory is valid or run with --debug to trace failures.")
        sys.exit(1)

if __name__ == "__main__":
    main()
