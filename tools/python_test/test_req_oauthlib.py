import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('requests-oauthlib')
        print(f"requests-oauthlib version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-requests-oauthlib is not installed.")
        sys.exit(1)

    # Test the core OAuth2 workflow
    try:
        from requests_oauthlib import OAuth2Session
        
        print("Initializing OAuth2Session...")
        client_id = "solus_test_client"
        scope = ["profile", "email"]
        
        # Instantiate the session
        session = OAuth2Session(client_id, scope=scope)
        
        # Generate an authorization URL and state token
        # This exercises the internal oauthlib URL building and cryptography logic
        auth_url, state = session.authorization_url("https://example.com/oauth/authorize")
        
        print("Success: OAuth2Session initialized and generated an authorization request!")
        print(f" -> State Token generated: {state}")
        print(f" -> Authorization URL: {auth_url}")
        
        if "client_id=solus_test_client" in auth_url and "scope=profile+email" in auth_url:
            print("Success: Scope and Client ID were correctly encoded into the URL.")
        else:
            print("Failed: URL encoding did not match expected output.")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import requests-oauthlib: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
