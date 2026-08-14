import importlib.metadata
import secretstorage
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('secretstorage')
        print(f"secretstorage version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-secretstorage is not installed.")
        sys.exit(1)

    # Test D-Bus Initialization and Module Loading
    try:
        print("Attempting to initialize D-Bus connection...")
        connection = secretstorage.dbus_init()
        print("Success: Initialized D-Bus connection!")
        
        # Try to fetch the default keyring collection
        collection = secretstorage.get_default_collection(connection)
        print(f"Success: Connected to default collection -> {collection}")
        
    except secretstorage.exceptions.SecretServiceNotAvailableException:
        print("\nSuccess: Module imported and parsed correctly!")
        print("Warning: Secret Service daemon is not running in this environment.")
        print("(This is completely expected if you are running this inside a headless build chroot or without a GUI session).")
        
    except Exception as e:
        print(f"\nTest failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
