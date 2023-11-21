import asyncio

async def handle_client(reader, writer):
    client_address = writer.get_extra_info('peername')
    print(f"Accepted from {client_address}")

    while True:
        data = await reader.read(100)
        if not data:
            break

        message = data.decode()
        print(f"Echo to {client_address}: {message}")

        writer.write(data)
        await writer.drain()

    print(f"Connection with {client_address} closed.")
    writer.close()

async def main():
    ip_address = input("Enter the IP address: ")
    port = int(input("Enter the port number: "))

    server = await asyncio.start_server(
        handle_client, ip_address, port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

