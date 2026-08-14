import importlib.metadata
import sys

def main():
    # Verify the package is installed
    try:
        version = importlib.metadata.version('PyQt5-sip')
        print(f"PyQt5-sip installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pyqt5-sip is not installed in the environment.")
        sys.exit(1)

    # Test importing and C-extension execution
    try:
        # It installs into the PyQt5 namespace
        from PyQt5 import sip
        
        print("Testing PyQt5.sip C-extension runtime...")
        
        # Pull the compiled SIP version string directly from the C-extension
        sip_version = sip.SIP_VERSION_STR
        print(f" -> Compiled SIP ABI Version: {sip_version}")
        
        if isinstance(sip_version, str) and len(sip_version) > 0:
            print(" -> Success: The PyQt5-sip C-extension loaded and executed perfectly!")
        else:
            print(" -> Failed: SIP_VERSION_STR returned invalid data.")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import PyQt5.sip (Is python3-qt5 installed?): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
