import importlib.metadata
import send2trash
import tempfile
import os
import shutil

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('send2trash')
        print(f"send2trash version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-send2trash is not installed.")
        return

    # Setup a sandboxed XDG environment so we don't pollute the real desktop trash
    base_dir = os.path.abspath("test_sandbox")
    fake_xdg_data = os.path.join(base_dir, "xdg_data")
    os.makedirs(fake_xdg_data, exist_ok=True)
    os.environ["XDG_DATA_HOME"] = fake_xdg_data

    try:
        # Create a dummy file inside our sandbox (avoids /tmp mount point issues)
        dummy_file_path = os.path.join(base_dir, "dummy_to_delete.txt")
        with open(dummy_file_path, "w") as f:
            f.write("This file belongs in the trash.")
            
        print(f"Created temporary file at: {dummy_file_path}")
        
        # Send it to the trash
        print("Sending to trash...")
        send2trash.send2trash(dummy_file_path)
        
        # Verify it was removed from the original location
        if not os.path.exists(dummy_file_path):
            print("Success: File was successfully moved to the system trash!")
            
            # Verify it actually ended up in our fake XDG trash bin
            trash_files_dir = os.path.join(fake_xdg_data, "Trash", "files")
            if os.path.exists(trash_files_dir) and os.listdir(trash_files_dir):
                print(f"Success: Verified the file is resting safely in {trash_files_dir}")
        else:
            print("Failed: File still exists at the original location.")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")
        
    finally:
        # Clean up our sandbox completely
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

if __name__ == '__main__':
    main()
