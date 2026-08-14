import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pyperclip')
        print(f"pyperclip installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pyperclip is not installed.")
        sys.exit(1)

    # Test the API
    try:
        import pyperclip
        
        print("Testing pyperclip module functionality...")
        
        # Check if the environment has a clipboard mechanism available (X11/Wayland)
        if not pyperclip.is_available():
            print(" -> Notice: No clipboard mechanism found (Expected in a headless/chroot environment).")
            print(" -> Success: Module imported and API responded correctly to headless state!")
            sys.exit(0)
            
        # If run on a real host machine, test the round-trip copy/paste
        test_string = "solus_clipboard_test_12345"
        
        print(" -> Clipboard mechanism found! Testing copy/paste...")
        pyperclip.copy(test_string)
        
        result = pyperclip.paste()
        
        if result == test_string:
            print(" -> Success: Text copied and pasted flawlessly!")
        else:
            print(f" -> Failed: Clipboard returned '{result}' instead of '{test_string}'")
            sys.exit(1)
            
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
