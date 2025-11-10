# async_client.py
import asyncio

HOST = "192.168.1.34"  # your PC's local IP
PORT = 65432

async def receive_messages(reader):
    """Continuously read messages from server."""
    while True:
        data = await reader.readline()
        if not data:
            print("Disconnected from server.")
            break
        print(data.decode().strip())

async def send_messages(writer):
    """Send user input to server."""
    loop = asyncio.get_event_loop()
    while True:
        msg = await loop.run_in_executor(None, input, "> ")
        writer.write((msg + "\n").encode())
        await writer.drain()

        if msg.lower() in ("quit", "exit", "bye"):
            break

async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print("Connected to async chat server.")

    # Run sender + receiver concurrently
    await asyncio.gather(
        receive_messages(reader),
        send_messages(writer)
    )

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
