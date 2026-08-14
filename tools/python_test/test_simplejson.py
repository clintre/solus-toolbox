import importlib.metadata
import simplejson

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('simplejson')
        print(f"simplejson version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-simplejson is not installed.")
        return

    try:
        # Check if the newly rewritten C-extension initialized
        if getattr(simplejson, '_speedups', None):
            print("Success: C-extension (_speedups) successfully loaded!")
        else:
            print("Warning/Failed: C-extension did NOT load. Falling back to pure Python.")
            print("Make sure the C compiler flags and %python3_cb build macros are correct.")

        # Test the newly optimized C-level indent encoding
        data = {
            'status': 'ok',
            'nested': [1, 2, {'key': 'value'}]
        }
        
        output = simplejson.dumps(data, indent=2)
        if '"key": "value"' in output:
            print("Success: Data serialized with indent correctly.")
        else:
            print("Failed: Output was malformed.")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == '__main__':
    main()
