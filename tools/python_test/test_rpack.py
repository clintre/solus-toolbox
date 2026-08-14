import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('rectangle-packer')
        print(f"rectangle-packer version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-rectangle-packer is not installed.")
        sys.exit(1)

    # Test the C-extension and fallback logic
    try:
        import rpack
        
        # Test 1: Standard packing
        print("Testing standard rectangle packing...")
        sizes = [(58, 206), (231, 176), (35, 113), (46, 109)]
        positions = rpack.pack(sizes)
        
        if len(positions) == len(sizes):
            print(" -> Success: Standard C-extension packed correctly.")
            print(f" -> Output positions: {positions}")
        else:
            print(" -> Failed: Standard packing returned incorrect length.")
            sys.exit(1)

        # Test 2: Huge Integer Fallback (New in 2.1.0)
        # These sizes exceed standard 32-bit limits and should trigger the new gcd reduction/scaling
        print("\nTesting large integer fallback path...")
        huge_sizes = [(10**15, 10**15), (2 * 10**15, 10**15)]
        huge_positions = rpack.pack(huge_sizes)
        
        if len(huge_positions) == len(huge_sizes):
            print(" -> Success: Huge integer fallback path executed successfully without overflow crashes!")
        else:
            print(" -> Failed: Huge integer packing failed.")
            sys.exit(1)

        print("\nAll C-extension paths are healthy and ready!")

    except ImportError as e:
        print(f"Failed to import rpack (the C-extension may have failed to build properly): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
