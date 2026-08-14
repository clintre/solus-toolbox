import importlib.metadata
import argparse
import shtab

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('shtab')
        print(f"shtab version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-shtab is not installed.")
        return

    # Setup a dummy ArgumentParser
    try:
        parser = argparse.ArgumentParser(description="Test App")
        parser.add_argument('--foo', help="Enable foo feature")
        parser.add_argument('--bar', choices=['a', 'b'], help="Select bar mode")
        print("Success: Initialized ArgumentParser.")
        
        # Test Bash completion generation
        bash_script = shtab.complete(parser, shell="bash")
        if "--foo" in bash_script and "--bar" in bash_script:
            print("Success: Generated valid bash completion script.")
        else:
            print("Failed: Bash script was malformed or missing arguments.")
            
        # Test Zsh completion generation
        zsh_script = shtab.complete(parser, shell="zsh")
        if "--foo" in zsh_script and "--bar" in zsh_script:
            print("Success: Generated valid zsh completion script.")
        else:
            print("Failed: Zsh script was malformed or missing arguments.")

    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == '__main__':
    main()
