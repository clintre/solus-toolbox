import tomlkit
import importlib.metadata

def main():
    print(f"tomlkit version: {importlib.metadata.version('tomlkit')}")

    # Create a TOML document with comments and specific whitespace
    original_toml = """
# This is a config file
[tool.poetry]
name = "my_package"
version = "1.0.0" # Current version

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""
    print("\n--- Original TOML ---")
    print(original_toml.strip())

    # Parse the document
    doc = tomlkit.parse(original_toml)

    # Modify the document
    doc["tool"]["poetry"]["version"] = "1.1.0"
    doc["tool"]["poetry"].add(tomlkit.comment("Version bumped by script"))

    # Serialize back to a string and ensure comments/whitespace are preserved
    modified_toml = tomlkit.dumps(doc)
    
    print("\n--- Modified TOML ---")
    print(modified_toml.strip())
    
    # Verify the modification logic
    if 'version = "1.1.0" # Current version' in modified_toml:
        print("\nSuccess: Modified the value while preserving inline comments!")
    else:
        print("\nFailed: Lost inline formatting during modification.")

if __name__ == '__main__':
    main()
