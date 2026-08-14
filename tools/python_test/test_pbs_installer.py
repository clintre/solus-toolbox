import sys
import importlib.metadata

def main():
    # Verify Version
    try:
        # Note: The package uses an underscore when queried or imported
        version = importlib.metadata.version('pbs_installer')
        print(f"pbs-installer installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pbs-installer is not installed.")
        sys.exit(1)

    # Test the API
    try:
        import pbs_installer
        
        print("Testing pbs-installer API...")
        
        # Test if the core download resolution function is available
        if hasattr(pbs_installer, 'get_download_link') and callable(pbs_installer.get_download_link):
            print(" -> Success: pbs_installer API is functioning (get_download_link is available)!")
        else:
            print(" -> Failed: The 'get_download_link' function was not found in the module.")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import pbs_installer: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
