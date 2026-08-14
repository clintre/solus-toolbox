import sys
import importlib.metadata
import subprocess

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('wheel')
        print(f"wheel installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-wheel is not installed.")
        sys.exit(1)

    # Test the API (Using a supported, public module)
    try:
        from wheel.wheelfile import WheelFile
        print(" -> Success: Python API for wheel.wheelfile loaded perfectly!")
    except ImportError as e:
        print(f"Failed to import wheel API: {e}")
        sys.exit(1)

    # Test the CLI
    print("Testing the wheel CLI...")
    try:
        result = subprocess.run(
            ['wheel', 'version'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f" -> Success: The CLI is operational (Output: {result.stdout.strip()})!")
    except subprocess.CalledProcessError as e:
        print(f"Failed: The wheel CLI returned an error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("Failed: The 'wheel' executable was not found in the PATH.")
        sys.exit(1)

if __name__ == '__main__':
    main()
