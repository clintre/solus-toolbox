import importlib.metadata
import os
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('rarfile')
        print(f"rarfile version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-rarfile is not installed.")
        sys.exit(1)

    # Test the core module and parsing logic
    dummy_path = "test_dummy.rar"
    try:
        import rarfile
        
        # Create a dummy file that is deliberately NOT a RAR archive
        with open(dummy_path, "wb") as f:
            f.write(b"This is definitely not a valid RAR archive payload.")
            
        print("Testing RAR parser on an invalid archive...")
        
        try:
            # This forces rarfile to attempt to parse the magic headers
            rf = rarfile.RarFile(dummy_path)
            print("Failed: RarFile accepted a completely invalid file!")
            sys.exit(1)
        except rarfile.NotRarFile:
            print(" -> Success: Correctly identified and rejected invalid RAR file (NotRarFile exception caught).")
            
        except Exception as e:
            print(f" -> Failed: Threw an unexpected exception type: {type(e).__name__}: {e}")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import rarfile: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        if os.path.exists(dummy_path):
            os.remove(dummy_path)

if __name__ == '__main__':
    main()
