import warnings
from deprecated import deprecated

# Apply the decorator (which relies on wrapt under the hood)
@deprecated(version='1.0', reason="This function is obsolete. Use new_function() instead.")
def old_function():
    return "Running old function."

def main():
    # Catch and print the warning to verify it triggers correctly
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        result = old_function()
        print(result)
        
        if len(w) == 1:
            print(f"Success! Caught deprecation warning: {w[-1].message}")
        else:
            print("Error: No deprecation warning was triggered.")

if __name__ == '__main__':
    main()
