import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('setuptools-rust')
        print(f"setuptools-rust version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-setuptools-rust is not installed.")
        sys.exit(1)

    # Test core module import and instantiation
    try:
        from setuptools_rust import RustExtension, Binding
        
        # Test instantiation of a RustExtension to ensure the API is fully functional
        ext = RustExtension(
            target="solus_rust_ext",
            path="Cargo.toml",
            binding=Binding.PyO3
        )
        print("Success: Successfully imported setuptools_rust and instantiated a RustExtension.")
        print(f"Extension details -> Target: {ext.target}, Binding: {ext.binding}")
        
    except ImportError as e:
        print(f"Failed to import setuptools_rust: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed during instantiation: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
