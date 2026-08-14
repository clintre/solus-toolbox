import sys
import importlib.metadata
from io import BytesIO

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pycurl')
        print(f"pycurl installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pycurl is not installed.")
        sys.exit(1)

    # Test the API
    try:
        import pycurl
        
        print(f" -> Linked against system libcurl version: {pycurl.version}")
        print("Testing pycurl HTTPS fetch functionality...")
        
        buffer = BytesIO()
        c = pycurl.Curl()
        
        # Configure a standard HTTPS GET request
        c.setopt(c.URL, 'https://example.com')
        c.setopt(c.WRITEDATA, buffer)
        
        # Execute the request
        c.perform()
        status_code = c.getinfo(c.RESPONSE_CODE)
        
        if status_code == 200:
            print(" -> Success: PycURL fetched example.com perfectly!")
        else:
            print(f" -> Failed: Received unexpected HTTP {status_code}")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import pycurl (check your libcurl linkage): {e}")
        sys.exit(1)
    except pycurl.error as e:
        print(f"Test failed with a PycURL networking error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)
    finally:
        try:
            c.close()
        except:
            pass

if __name__ == '__main__':
    main()
