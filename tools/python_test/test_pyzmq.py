import importlib.metadata
import sys
import time

def main():
    # Verify Version
    try:
        version = importlib.metadata.version('pyzmq')
        print(f"pyzmq installed version: {version}")
    except importlib.metadata.PackageNotFoundError:
        print("Failed: python-pyzmq is not installed.")
        sys.exit(1)

    # Test the API
    try:
        import zmq
        
        print("Testing pyzmq C-extension and message passing...")
        print(f" -> Linked against system libzmq version: {zmq.zmq_version()}")
        
        # Create a context
        context = zmq.Context()
        
        # Set up a Publisher
        pub_socket = context.socket(zmq.PUB)
        pub_socket.bind("tcp://127.0.0.1:5555")
        
        # Set up a Subscriber
        sub_socket = context.socket(zmq.SUB)
        sub_socket.connect("tcp://127.0.0.1:5555")
        sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        
        # Give sockets a moment to handshake
        time.sleep(0.1)
        
        # Send a message
        test_msg = b"solus-pyzmq-test"
        pub_socket.send(test_msg)
        
        # Receive the message (with a timeout so we don't hang if it fails)
        if sub_socket.poll(1000):
            recv_msg = sub_socket.recv()
            if recv_msg == test_msg:
                print(" -> Success: Message published and subscribed flawlessly!")
            else:
                print(f" -> Failed: Received unexpected data: {recv_msg}")
                sys.exit(1)
        else:
            print(" -> Failed: Subscriber timed out waiting for the message.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            pub_socket.close()
            sub_socket.close()
            context.term()
        except:
            pass

if __name__ == '__main__':
    main()
