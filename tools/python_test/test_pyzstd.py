import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pyzstd')
        print(f"pyzstd version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pyzstd is not installed.")
        sys.exit(1)

    # Test core compression/decompression loop
    try:
        import pyzstd
        
        print("Testing Zstandard compression wrapper...")
        original_data = b"Hello, Solus! This is a pure-Python Zstandard wrapper test. " * 50
        
        # Compress
        compressed = pyzstd.compress(original_data)
        
        # Decompress
        decompressed = pyzstd.decompress(compressed)
        
        if decompressed == original_data:
            print(" -> Success: Data compressed and decompressed flawlessly!")
            print(f" -> Original size: {len(original_data)} bytes")
            print(f" -> Compressed size: {len(compressed)} bytes")
            
            # Since 0.19.0 routes to compression.zstd, let's peek under the hood
            if hasattr(pyzstd, 'CFFI') or 'cffi' in sys.modules:
                print(" -> Note: Running via CFFI fallback.")
            else:
                print(" -> Note: Running via native CPython backend.")
        else:
            print(" -> Failed: Decompressed data did not match the original payload.")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import pyzstd: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
