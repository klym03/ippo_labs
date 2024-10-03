import json

import asyncpg


from dotenv.main import load_dotenv
import os

load_dotenv()
DB_NAME = os.environ['POSTGRES_DB']
DB_USERNAME = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_HOST = os.environ['POSTGRES_HOST']
DB_PORT = os.environ['POSTGRES_PORT']
pool = asyncpg.create_pool()


async def start_db() -> None:
    global pool
    pool = await asyncpg.create_pool(database=DB_NAME, user=DB_USERNAME,
                                     password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
              user_id BIGINT PRIMARY KEY
            )
          """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS orders(
              id SERIAL PRIMARY KEY,
              pdf_file VARCHAR(255) NOT NULL,
              variant VARCHAR(255) NOT NULL,
              student_group VARCHAR(255) NOT NULL,
              user_id BIGINT REFERENCES users(user_id)
            )
          """)


