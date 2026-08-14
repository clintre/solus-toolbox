import sys
import importlib.metadata

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pycryptodome')
        print(f"PyCryptodome installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pycryptodome is not installed.")
        sys.exit(1)

    # Test AES Decryption (Testing the yt-dlp/streamlink use-case)
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
        
        print("Testing PyCryptodome AES-CBC functionality...")
        
        key = b'Solus16ByteKey!!'
        data = b'Test video stream payload'
        
        # Encrypt
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = cipher.iv
        
        # Decrypt
        decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)
        pt_bytes = unpad(decrypt_cipher.decrypt(ct_bytes), AES.block_size)
        
        if pt_bytes == data:
            print(" -> Success: AES payload was perfectly encrypted and decrypted!")
        else:
            print(" -> Failed: Decrypted payload did not match the original.")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import PyCryptodome (Check your C-extension build): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
