import os
import shutil
import importlib.metadata
from sphinx.application import Sphinx

def main():
    # Verify Version
    version = importlib.metadata.version('sphinx')
    print(f"Sphinx version: {version}")

    # Setup a dummy Sphinx project directory
    src_dir = "test_sphinx_src"
    out_dir = "test_sphinx_out"
    doctree_dir = "test_sphinx_doctrees"
    
    os.makedirs(src_dir, exist_ok=True)
    
    # Create a basic conf.py enabling the newly rewritten autodoc
    with open(os.path.join(src_dir, "conf.py"), "w") as f:
        f.write("project = 'Test'\n")
        f.write("extensions = ['sphinx.ext.autodoc']\n")
    
    # Create an index.rst that tries to autodoc a standard library module
    with open(os.path.join(src_dir, "index.rst"), "w") as f:
        f.write("Test Docs\n=========\n\n")
        f.write(".. automodule:: json\n   :members:\n")

    try:
        # Initialize the Sphinx application via Python API
        print("Initializing Sphinx application and autodoc...")
        app = Sphinx(
            srcdir=src_dir,
            confdir=src_dir,
            outdir=out_dir,
            doctreedir=doctree_dir,
            buildername="html",
            warningiserror=True, # Fail if autodoc throws a warning
        )
        
        # Build the HTML documentation
        print("Building HTML output...")
        app.build(force_all=True)
        
        # Verify output exists
        if os.path.exists(os.path.join(out_dir, "index.html")):
            print("Success: Built HTML documentation using Sphinx 9.1.0's autodoc engine!")
        else:
            print("Failed: HTML output not found.")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")
        
    finally:
        # Cleanup
        for d in [src_dir, out_dir, doctree_dir]:
            if os.path.exists(d):
                shutil.rmtree(d)

if __name__ == '__main__':
    main()
