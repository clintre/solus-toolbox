import importlib.metadata
import numpy as np
import tifffile

def main():
    # Verify Version
    version = importlib.metadata.version('tifffile')
    print(f"tifffile version: {version}")

    try:
        # Create dummy image data (e.g., a 3-page 8-bit TIFF, 100x100 pixels)
        print("Generating mock multipage TIFF data...")
        data = np.random.randint(0, 255, (3, 100, 100), dtype=np.uint8)
        
        # Write data to a temporary TIFF file
        temp_file = 'test_multipage.tiff'
        tifffile.imwrite(temp_file, data, photometric='minisblack')
        print(f"Success: Wrote mock array to {temp_file}")
        
        # Read it back using the primary API scikit-image uses
        read_data = tifffile.imread(temp_file)
        
        if np.array_equal(data, read_data):
            print(f"Success: Verified read/write integrity! Array shape: {read_data.shape}")
        else:
            print("Error: Read data does not match written data.")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == '__main__':
    main()
