import asyncpg
import asyncio
pool = asyncpg.create_pool()
from dotenv.main import load_dotenv
import os
import json

load_dotenv()
DB_NAME = os.environ['POSTGRES_DB']
DB_USERNAME = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_HOST = os.environ['POSTGRES_HOST']
DB_PORT = os.environ['POSTGRES_PORT']


async def connect_db() -> None:
    global pool
    pool = await asyncpg.create_pool(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

async def add_user(user_id: int) -> None:
    async with pool.acquire() as conn:
        await conn.execute('INSERT INTO users(user_id) VALUES($1)', user_id)

async def get_user(user_id: int) -> dict:
    async with pool.acquire() as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
        return user

async def add_order(pdf_file: str, variant: str, student_group: str, user_id: int ) -> None:
    async with pool.acquire() as conn:
        await conn.execute('INSERT INTO orders(pdf_file, variant, student_group, user_id) VALUES($1, $2, $3, $4)', pdf_file, variant, student_group, user_id)

async def get_order(user_id: int) -> dict:
    async with pool.acquire() as conn:
        order = await conn.fetchrow('SELECT * FROM orders WHERE user_id = $1', user_id)
        return order