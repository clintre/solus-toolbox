import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('scikit-build-core')
        print(f"scikit-build-core version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-scikit-build-core is not installed.")
        sys.exit(1)

    # Test the core PEP 517 build backend hooks
    try:
        from scikit_build_core import build
        
        # Verify the required backend functions are exposed
        required_hooks = [
            'build_wheel',
            'build_sdist',
            'get_requires_for_build_wheel'
        ]
        
        missing = [hook for hook in required_hooks if not hasattr(build, hook)]
        
        if not missing:
            print("Success: Core PEP 517 build hooks are intact and ready for CMake builds!")
            print(f"Loaded backend module: {build.__file__}")
        else:
            print(f"Failed: The build backend is missing expected hooks: {missing}")
            
    except ImportError as e:
        print(f"Failed to import the scikit-build-core build backend: {e}")
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")

if __name__ == '__main__':
    main()
