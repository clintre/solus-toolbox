import importlib.metadata
from traitlets import HasTraits, Int, Unicode, TraitError
from traitlets import Path as TraitPath
import pathlib

def main():
    # Verify Version
    version = importlib.metadata.version('traitlets')
    print(f"traitlets version: {version}")

    # Define a configuration class using Traits
    class JupyterMockConfig(HasTraits):
        port = Int(8888, help="The port the server will listen on.")
        ip = Unicode('localhost', help="The IP address the server will listen on.")
        
        # Testing the NEW 5.16.0 feature
        work_dir = TraitPath(allow_none=True)

    config = JupyterMockConfig()

    # Test validation functionality
    print("Testing trait validation...")
    try:
        # This should succeed
        config.port = 9000
        config.work_dir = pathlib.Path('/tmp')
        print(f"Success: Validated port ({config.port}) and path ({config.work_dir})")
        
        # This should fail and throw a TraitError (passing string to Int)
        config.port = "not_a_number"
    except TraitError:
        print("Success: Caught TraitError when passing invalid type.")
    except Exception as e:
        print(f"Failed with unexpected error: {e}")

if __name__ == '__main__':
    main()
