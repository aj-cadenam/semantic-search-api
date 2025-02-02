import asyncpg
import pgvector


class DBAdapter:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)
        await self._initialize_pgvector()

    async def _initialize_pgvector(self):
        async with self.pool.acquire() as connection:
            await connection.execute("CREATE EXTENSION IF NOT EXISTS vector")

    async def close(self):
        await self.pool.close()

    async def execute(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def fetchval(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchval(query, *args)


# Usage example:
# adapter = DBAdapter(dsn="postgresql://user:password@localhost/dbname")
# await adapter.connect()
# await adapter.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, vector vector(3))")
# await adapter.close()
