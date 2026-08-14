import importlib.metadata
import subprocess
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('sip')
        print(f"sip version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-sip is not installed.")
        sys.exit(1)

    # Test the core module import
    try:
        import sipbuild
        print("Success: Successfully imported the sipbuild module.")
    except ImportError as e:
        print(f"Failed to import sipbuild: {e}")
        sys.exit(1)

    # Test the command-line executables
    print("Testing command-line tools...")
    tools = ['sip-build', 'sip-wheel', 'sip-install']
    
    for tool in tools:
        try:
            # Running with --help to ensure the entry points are valid and don't crash
            result = subprocess.run([tool, '--help'], capture_output=True, text=True, check=True)
            if "Usage:" in result.stdout or "usage:" in result.stdout:
                print(f"Success: {tool} CLI is operational.")
            else:
                print(f"Failed: {tool} CLI did not return expected help text.")
        except FileNotFoundError:
            print(f"Failed: The '{tool}' executable was not found in PATH. Check entry points.")
        except subprocess.CalledProcessError as e:
            print(f"Failed: {tool} CLI threw an error. {e}")

if __name__ == '__main__':
    main()
