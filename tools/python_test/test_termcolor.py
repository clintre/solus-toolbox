import sys
import importlib.metadata
from termcolor import colored, cprint, can_colorize

def main():
    # Verify Version
    version = importlib.metadata.version('termcolor')
    print(f"termcolor version: {version}")

    # Test the new public API (checking for color support)
    color_support = can_colorize()
    print(f"Terminal supports color: {color_support}")

    # Test standard ANSI color formatting
    print(colored("Success: This is standard green text.", "green", attrs=["bold"]))

    # Test the NEW True Color (RGB) support added in the 3.x series
    try:
        # Foreground tuple, Background tuple
        cprint("Success: This text uses true RGB color tuples!", (250, 150, 100), (40, 50, 60))
    except Exception as e:
        print(f"Failed: True color RGB implementation threw an error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
