import sys

def main():
    print("Testing Printrun imports...")
    try:
        # Import the core library
        import printrun.printcore
        print(" -> Success: Loaded printrun.printcore")
        
        # Import the GUI components (which trigger the puremagic image lookups)
        import printrun.pronterface
        print(" -> Success: Loaded printrun.pronterface")
        
        print("\nAll Printrun modules loaded flawlessly with puremagic 2.2.0!")
        
    except ImportError as e:
        print(f"Failed to import Printrun modules: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
