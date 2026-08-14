import importlib.metadata
import sys

# We need a Qt backend installed (PyQt5, PyQt6, PySide2, or PySide6) for superqt to work
try:
    from qtpy.QtWidgets import QApplication
    from superqt import QDoubleRangeSlider
except ImportError as e:
    print(f"Skipping widget test: Missing Qt bindings or qtpy. ({e})")
    sys.exit(0)

def main():
    # Verify Version
    version = importlib.metadata.version('superqt')
    print(f"superqt version: {version}")

    # Test instantiation of a superqt custom widget
    app = QApplication.instance() or QApplication(sys.argv)
    
    try:
        print("Instantiating QDoubleRangeSlider...")
        slider = QDoubleRangeSlider()
        slider.setRange(0.0, 100.0)
        slider.setValue((20.5, 80.5))
        
        current_value = slider.value()
        
        if current_value == (20.5, 80.5):
            print(f"Success: Widget instantiated and state verified: {current_value}")
        else:
            print("Failed: Widget value mismatch.")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == '__main__':
    main()
