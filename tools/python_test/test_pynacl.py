import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('PyNaCl')
        print(f"PyNaCl installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pynacl is not installed.")
        sys.exit(1)

    # Test the API
    try:
        import nacl.utils
        from nacl.public import PrivateKey, Box
        
        print("Testing PyNaCl encryption functionality...")
        
        # Generate two keypairs
        alice = PrivateKey.generate()
        bob = PrivateKey.generate()
        
        # Create a Box for Alice to send a message to Bob
        alice_box = Box(alice, bob.public_key)
        
        message = b"Solus PyNaCl Test Message"
        encrypted = alice_box.encrypt(message)
        
        # Create a Box for Bob to decrypt Alice's message
        bob_box = Box(bob, alice.public_key)
        decrypted = bob_box.decrypt(encrypted)
        
        if decrypted == message:
            print(" -> Success: PyNaCl successfully generated keys, encrypted, and decrypted the message!")
        else:
            print(" -> Failed: Decrypted message does not match.")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import PyNaCl: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
