import asyncio
from jupyter_client.manager import AsyncKernelManager

async def test_jupyter_client():
    print("Starting KernelManager...")
    km = AsyncKernelManager(kernel_name='python3')
    await km.start_kernel()
    print(f"Kernel started. Is alive: {await km.is_alive()}")
    
    # Start the client channels
    client = km.client()
    client.start_channels()
    
    # Wait briefly to let Tornado event loop initialize connections
    await asyncio.sleep(1)
    
    print("Executing code via Tornado's asynchronous I/O event loop...")
    msg_id = client.execute("print('Hello from jupyter-client with patched Tornado!')")
    
    # Grab the response
    reply = client.get_shell_msg(timeout=5)
    print("Execution reply status:", reply['content']['status'])
    
    # Clean up
    client.stop_channels()
    await km.shutdown_kernel()
    print("Kernel shut down successfully.")

if __name__ == '__main__':
    asyncio.run(test_jupyter_client())
    
