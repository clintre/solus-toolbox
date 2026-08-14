import importlib.metadata
import subprocess

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('sphinxygen')
        print(f"sphinxygen version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-sphinxygen is not installed.")
        return

    # Test the Python API
    try:
        import sphinxygen
        print("Success: Successfully imported the sphinxygen Python module.")
    except ImportError as e:
        print(f"Failed to import sphinxygen: {e}")

    # Test the Command-Line Interface
    print("Testing command-line executable...")
    try:
        # Run `sphinxygen --help` to ensure the entry point is valid
        result = subprocess.run(['sphinxygen', '--help'], capture_output=True, text=True, check=True)
        if "Usage:" in result.stdout or "usage:" in result.stdout:
            print("Success: sphinxygen CLI is operational and returned help text.")
        else:
            print("Failed: CLI did not return expected help text.")
    except FileNotFoundError:
        print("Failed: The 'sphinxygen' executable was not found in PATH. Check entry points.")
    except subprocess.CalledProcessError as e:
        print(f"Failed: CLI threw an error. {e}")

if __name__ == '__main__':
    main()
