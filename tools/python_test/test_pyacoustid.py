import sys
import importlib.metadata

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pyacoustid')
        print(f"pyacoustid installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pyacoustid is not installed.")
        sys.exit(1)

    # Test Chromaprint linkage
    try:
        import chromaprint
        
        print("Testing pyacoustid / chromaprint linkage...")
        
        # Verify the Python wrapper can communicate with the C library
        if chromaprint._libchromaprint is None:
            print(" -> Failed: The underlying Chromaprint C library could not be found.")
            sys.exit(1)
            
        # Get the version string directly from the C library
        c_version = chromaprint._libchromaprint.chromaprint_get_version()
        version_str = c_version.decode('utf-8')
        
        print(f" -> Success: pyacoustid successfully loaded the system Chromaprint library (v{version_str})!")
        
    except ImportError as e:
        print(f"Failed to import pyacoustid: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
