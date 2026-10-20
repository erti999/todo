import asyncio
from sqlalchemy import text
from app.database import engine

async def main():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        print("POSTGR:", result.scalar())
    await engine.dispose()

asyncio.run(main())