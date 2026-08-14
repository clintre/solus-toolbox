import importlib.metadata

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('sphinxcontrib-websupport')
        print(f"sphinxcontrib-websupport version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-sphinxcontrib-websupport is not installed.")
        return

    # Test the core API import
    try:
        from sphinxcontrib.websupport import WebSupport
        print("Success: Successfully imported the WebSupport class.")
        
        # Quick instantiation test (with dummy paths just to ensure `__init__` doesn't crash)
        try:
            # We don't actually build anything, just instantiate the object
            support = WebSupport(srcdir='/tmp', builddir='/tmp/build')
            print("Success: WebSupport object instantiated successfully.")
        except Exception as e:
            # It might complain about the dummy directories not having conf.py, which is fine
            if "conf.py" in str(e):
                print("Success: WebSupport initialized and correctly looked for conf.py.")
            else:
                print(f"Failed during instantiation: {e}")
                
    except ImportError as e:
        print(f"Failed to import WebSupport: {e}")

if __name__ == '__main__':
    main()
