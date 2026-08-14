import importlib.metadata
import snowballstemmer

def main():
    # Verify Version
    version = importlib.metadata.version('snowballstemmer')
    print(f"snowballstemmer version: {version}")

    try:
        # List available algorithms
        algorithms = snowballstemmer.algorithms()
        print(f"Success: Found {len(algorithms)} stemming algorithms.")
        
        # Test the English stemmer
        stemmer = snowballstemmer.stemmer('english')
        
        test_words = ["connection", "connections", "connective", "connected", "connecting"]
        expected_stem = "connect"
        
        print(f"Stemming test words: {test_words}")
        results = stemmer.stemWords(test_words)
        
        print(f"Results: {results}")
        
        # Verify all words stemmed to 'connect'
        if all(word == expected_stem for word in results):
            print(f"Success: All words correctly stemmed to '{expected_stem}'.")
        else:
            print("Failed: Stemming results did not match expectations.")

    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == '__main__':
    main()
