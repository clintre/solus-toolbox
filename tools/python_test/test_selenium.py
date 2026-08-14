import importlib.metadata
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('selenium')
        print(f"selenium version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-selenium is not installed.")
        sys.exit(1)

    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        
        print("Success: Successfully imported selenium.")
        print("Testing headless browser initialization (this may take a moment if Selenium Manager needs to download a driver)...")
        
        # Setup headless Firefox (most likely to succeed on a Linux desktop natively)
        options = FirefoxOptions()
        options.add_argument("--headless")
        
        # We don't specify an executable path so Selenium Manager handles it automatically
        with webdriver.Firefox(options=options) as driver:
            # Navigate to a lightweight page
            driver.get("https://example.com")
            title = driver.title
            
            if "Example Domain" in title:
                print(f"Success: Headless browser spun up and retrieved title: '{title}'")
            else:
                print(f"Failed: Reached the page but got an unexpected title: '{title}'")
                
    except ImportError as e:
        print(f"Failed to import webdriver: {e}")
    except Exception as e:
        print(f"Test failed with exception: {e}")
        print("\nNote: If this failed due to a missing browser, ensure Firefox or Chrome is installed on the testing machine, or that it has internet access to download them.")

if __name__ == '__main__':
    main()
