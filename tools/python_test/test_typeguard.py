import importlib.metadata
from typeguard import typechecked, TypeCheckError

# Verify Version
print(f"Typeguard version: {importlib.metadata.version('typeguard')}")

# Test Core Functionality
@typechecked
def greet(name: str) -> str:
    return f"Hello, {name}!"

try:
    # This should trigger a TypeCheckError because we are passing an int instead of a str
    greet(123)
except TypeCheckError as e:
    print(f"Success! Typeguard caught the error: {e}")
