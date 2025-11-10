import asyncio

clients = set()

async def broadcast(message, sender_writer=None):
    """Send message to all connected client except sender"""
    deisconnected = []
    for writer in clients:
        if writer != sender_writer:
            try:
                writer.write(message.encode())
                await writer.drain()
            except ConnectionResetError:
                deisconnected.append(writer)
                
    for writer in deisconnected:
        clients.remove(writer)
        
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[NEW CONNECTION] {addr} connected")
    writer.write(b"Welcome to the async chat server!\n")
    await writer.drain()
    
    clients.add(writer)
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            
            message = data.decode().strip()
            print(f"[{addr}] {message}")
            
            if message.lower() in ("quit", "exit", "bye"):
                writer.write(b"Good bye!\n")
                await writer.drain()
                break
            
            reply = f"bot to {addr}: you said -> {message}\n"
            writer.write(reply.encode())
            await writer.drain()
            
            await broadcast(f"[{addr}] {message}\n", sender_writer=writer)
            
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
        
    print(f"[DISCONNECTED] {addr}")
    clients.remove(writer)
    writer.close()
    await writer.wait_closed()
    
async def main():
    host = "0.0.0.0"
    port = 65432
    server = await asyncio.start_server(handle_client, host,port)
    ip = "192.168.1.34"
    
    print(f"[STARTED] Async chat server on {ip}: {port}")
    async with server:
        await server.serve_forever()
        
if __name__ == "__main__":
    asyncio.run(main())