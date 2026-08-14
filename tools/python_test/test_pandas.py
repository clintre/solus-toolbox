import sys
import importlib.metadata

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pandas')
        print(f"pandas installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pandas is not installed.")
        sys.exit(1)

    # Test the API
    try:
        import pandas as pd
        
        print("Testing pandas DataFrame creation and C-extension linkage...")
        
        # Instantiate a simple DataFrame to verify basic functionality
        data = {'Name': ['Solus', 'Linux'], 'Score': [100, 99]}
        df = pd.DataFrame(data)
        
        # Perform a basic operation
        mean_score = df['Score'].mean()
        
        if mean_score == 99.5:
            print(" -> Success: pandas successfully created a DataFrame and computed the mean!")
        else:
            print(f" -> Failed: Unexpected mean value computed. Got: {mean_score}")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import pandas: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
