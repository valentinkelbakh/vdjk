import asyncio
from app.loader import server

if __name__ == "__main__":
    asyncio.run(server.serve())
