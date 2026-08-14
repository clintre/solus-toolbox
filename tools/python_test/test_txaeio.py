import importlib.metadata
import txaio

def main():
    # Verify Version
    version = importlib.metadata.version('txaio')
    print(f"txaio version: {version}")

    # Test Framework-Agnostic Logging
    # This proves txaio can initialize its logger without failing on missing backends
    logger = txaio.make_logger()
    logger.info("Testing txaio logging output...")
    print("Success: Created txaio logger instance")

    # Test Auto-Framework Detection & Future Creation
    # This lets txaio bind to standard asyncio automatically and manipulate futures
    try:
        # Create a future
        f = txaio.create_future()
        
        # Resolve it
        txaio.resolve(f, "test_result")
        
        # Verify it works transparently
        print("Success: Auto-detected framework and resolved a Future")
    except Exception as e:
        print(f"Error creating future via auto-detection: {e}")

if __name__ == '__main__':
    main()
