import jupyter_client
from jupyter_client.manager import start_new_kernel

def main():
    print(f"jupyter_client version: {jupyter_client.__version__}")
    
    # Start a new local Python kernel using the corrected manager import
    print("Starting new Python kernel...")
    km, kc = start_new_kernel(kernel_name='python3')
    
    try:
        # Execute a simple Python command inside the kernel
        print("Executing test math in kernel...")
        kc.execute("result = 10 * 5")
        
        # Wait for the shell to confirm it processed the execution
        reply = kc.get_shell_msg(timeout=10)
        status = reply['content']['status']
        
        if status == 'ok':
            print("Success: Kernel processed the code successfully!")
        else:
            print(f"Error: Kernel execution failed with status: {status}")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")
            
    finally:
        # Clean up channels and shutdown the background process
        print("Shutting down kernel...")
        kc.stop_channels()
        km.shutdown_kernel()

if __name__ == '__main__':
    main()
