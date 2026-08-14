import importlib.metadata
import sys
import io

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pypdf')
        print(f"pypdf installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pypdf is not installed.")
        sys.exit(1)

    # Test the API for Nemo's use-case
    try:
        from pypdf import PdfWriter, PdfReader
        
        print("Testing pypdf metadata extraction...")
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        writer.add_metadata({"/Title": "Solus Test Document"})
        
        # Save to memory instead of disk
        pdf_stream = io.BytesIO()
        writer.write(pdf_stream)
        pdf_stream.seek(0)
        
        # Read it back
        reader = PdfReader(pdf_stream)
        title = reader.metadata.get("/Title")
        
        if title == "Solus Test Document":
            print(" -> Success: pypdf wrote and read PDF metadata successfully!")
        else:
            print(f" -> Failed: Expected 'Solus Test Document', got '{title}'")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Failed to import pypdf: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
