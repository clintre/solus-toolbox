import importlib.metadata
import os
from svglib.svglib import svg2rlg

def main():
    # Verify Version
    version = importlib.metadata.version('svglib')
    print(f"svglib version: {version}")

    # Create a very basic mock SVG file
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
    </svg>"""
    
    test_svg = "test_circle.svg"
    with open(test_svg, "w") as f:
        f.write(svg_content)
        
    try:
        # Test the core API used by reverse dependencies
        print("Parsing SVG to ReportLab Drawing...")
        drawing = svg2rlg(test_svg)
        
        if drawing is not None:
            # Check if it successfully parsed the bounds
            bounds = drawing.getBounds()
            print(f"Success: Parsed drawing with bounds {bounds}")
        else:
            print("Failed: svglib returned None")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")
    finally:
        if os.path.exists(test_svg):
            os.remove(test_svg)

if __name__ == '__main__':
    main()
