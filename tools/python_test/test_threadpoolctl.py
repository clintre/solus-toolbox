import importlib.metadata
from threadpoolctl import threadpool_info, threadpool_limits

def main():
    # Verify Version
    version = importlib.metadata.version('threadpoolctl')
    print(f"threadpoolctl version: {version}")

    try:
        # Get information about loaded threadpools
        print("\nScanning for active linear algebra / OpenMP libraries...")
        info = threadpool_info()
        
        if not info:
            print("Warning: No BLAS/OpenMP libraries detected in this environment.")
            print("This is normal if numpy/scipy are not installed in the build chroot.")
        else:
            print("Successfully detected the following backends:")
            for module in info:
                print(f" - {module['user_api']} ({module['internal_api']}): "
                      f"{module.get('num_threads')} threads max")

        # Test limiting functionality
        print("\nTesting thread limiting context manager...")
        with threadpool_limits(limits=1, user_api='blas'):
            limited_info = threadpool_info()
            print("Inside context manager, threads are limited to 1 (if libraries are present).")
            
        print("Success: Context manager executed without errors.")

    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == '__main__':
    main()
