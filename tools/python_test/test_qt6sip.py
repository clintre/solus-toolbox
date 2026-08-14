import importlib.metadata
import sys

def main():
    # Verify the package is installed via pip/metadata
    try:
        version = importlib.metadata.version('PyQt6-sip')
        print(f"PyQt6-sip installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pyqt6-sip is not installed in the environment.")
        sys.exit(1)

    # Test importing and ABI execution
    try:
        # It installs into the PyQt6 namespace
        from PyQt6 import sip
        
        print("Testing PyQt6.sip C-extension runtime...")
        
        # Pull the compiled SIP version string directly from the C-extension
        sip_version = sip.SIP_VERSION_STR
        print(f" -> Compiled SIP ABI Version: {sip_version}")
        
        # Verify the C-extension didn't crash and returns the expected string
        if isinstance(sip_version, str) and len(sip_version) > 0:
            print(" -> Success: The PyQt6-sip C-extension loaded and executed perfectly!")
        else:
            print(" -> Failed: SIP_VERSION_STR returned invalid data.")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import PyQt6.sip (Is python-qt6 installed?): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
