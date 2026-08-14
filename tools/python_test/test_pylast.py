import sys
import importlib.metadata

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pylast')
        print(f"pylast installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pylast is not installed.")
        sys.exit(1)

    # Test the API and Networking Initialization
    try:
        import pylast
        
        print("Testing pylast initialization and network setup...")
        
        # Test basic instantiation (without making a real network call requiring credentials)
        network = pylast.LastFMNetwork(
            api_key="dummy_api_key",
            api_secret="dummy_api_secret"
        )
        
        # Fetch a mock object to ensure the classes and HTTPX client instantiate correctly
        artist = network.get_artist("System of a Down")
        
        print(f" -> Success: pylast successfully initialized and created Artist object for: {artist.name}")
        
    except ImportError as e:
        print(f"Failed to import pylast (Did you add python-httpx to rundeps?): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
