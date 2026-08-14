import importlib.metadata
import os
import sys

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('reportlab')
        print(f"reportlab version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-reportlab is not installed.")
        sys.exit(1)

    # Test the Canvas and C-extensions
    try:
        from reportlab.pdfgen import canvas
        
        pdf_path = "solus_test_output.pdf"
        print("Creating a test PDF...")
        
        # Instantiate a basic canvas
        c = canvas.Canvas(pdf_path)
        
        # Draw some text (this relies on the internal text and font metrics machinery)
        c.drawString(100, 750, "Hello, Solus! This is a ReportLab 5.0.0 test.")
        
        # Save and close
        c.save()
        
        if os.path.exists(pdf_path):
            print(f"Success: Generated {pdf_path} successfully!")
            print(f"Filesize: {os.path.getsize(pdf_path)} bytes")
            # Cleanup
            os.remove(pdf_path)
        else:
            print("Failed: The PDF file was not created.")
            sys.exit(1)
        
    except ImportError as e:
        print(f"Failed to import reportlab (C-extensions might have failed to build): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
