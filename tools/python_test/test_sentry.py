import importlib.metadata
import sentry_sdk

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('sentry-sdk')
        print(f"sentry-sdk version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-sentry-sdk is not installed.")
        return

    # Setup a Dummy Transport to intercept network calls
    captured_events = []
    
    def dummy_transport(event):
        # Instead of sending to the internet, we just append to our list
        captured_events.append(event)

    try:
        # Initialize the SDK with the dummy transport
        sentry_sdk.init(
            dsn="https://dummy@sentry.example.com/1",
            transport=dummy_transport,
            traces_sample_rate=1.0
        )
        print("Success: Initialized sentry_sdk.")

        # Trigger an intentional exception
        try:
            1 / 0
        except ZeroDivisionError as e:
            sentry_sdk.capture_exception(e)
            
        # Verify the SDK intercepted and processed it
        sentry_sdk.flush() # Ensure the background queue is empty
        
        if captured_events:
            event = captured_events[0]
            exception_type = event.get("exception", {}).get("values", [{}])[0].get("type")
            
            if exception_type == "ZeroDivisionError":
                print("Success: SDK caught, formatted, and processed the ZeroDivisionError!")
            else:
                print(f"Warning: Event captured but exception type was {exception_type}")
        else:
            print("Failed: No events were captured by the dummy transport.")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == '__main__':
    main()
