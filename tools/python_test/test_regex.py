import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('regex')
        print(f"regex version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-regex is not installed.")
        sys.exit(1)

    # Test the C-extensions and advanced features
    try:
        import regex
        
        # Test 1: Standard matching
        print("Testing standard pattern matching...")
        match = regex.search(r'\b(solus)\b', 'Welcome to solus linux', flags=regex.IGNORECASE)
        if match and match.group(1).lower() == 'solus':
            print(" -> Success: Standard matching works.")
        else:
            print(" -> Failed: Standard matching did not return the expected result.")
            sys.exit(1)

        # Test 2: Fuzzy matching (This is unique to mrab-regex!)
        print("Testing fuzzy matching (substitution/insertion/deletion)...")
        # Find 'solus' with up to 1 error (e.g., 'solis')
        fuzzy_match = regex.search(r'(solus){e<=1}', 'Welcome to solis linux')
        if fuzzy_match and fuzzy_match.group(0) == 'solis':
            print(" -> Success: Fuzzy matching works perfectly!")
        else:
            print(" -> Failed: Fuzzy matching did not return the expected result.")
            sys.exit(1)

        # Test 3: Variable-length lookbehind (Standard re module fails on this)
        print("Testing variable-length lookbehind...")
        lookbehind_match = regex.search(r'(?<=a+b+)c', 'aaabbbc')
        if lookbehind_match and lookbehind_match.group(0) == 'c':
            print(" -> Success: Variable-length lookbehind works!")
        else:
            print(" -> Failed: Variable-length lookbehind did not work.")
            sys.exit(1)

        print("\nAll regex features tested successfully. The C-extensions are healthy!")

    except ImportError as e:
        print(f"Failed to import regex (the C-extension may have failed to build properly): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
