import asyncio
from typing import *

from os import getenv

import sqlalchemy 
from sqlalchemy import Date, func, insert, text, update, delete, select, Float, String, desc, asc
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from .models import pack_models

class Database:
	def __init__(self, conn_string: str=getenv('DB_CONN_STRING')) -> None:
		'''
conn_string: dialect+driver://username:password@host:port/database
		'''

		self.engine: AsyncEngine = create_async_engine(conn_string, pool_pre_ping=True)
		self.metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()

		models = pack_models(self.metadata)

		self.admins = models['admins']

	async def create_all(self):
		async with self.engine.begin() as conn:
			await conn.run_sync(self.metadata.create_all)
	
	def row_to_dict(self, rows: Union[object, List[object]]) -> Union[List[dict], dict]:
		''':rows: one row or list of rows'''
		if not rows: return rows 
		
		if type(rows) == list: return [row._mapping for row in rows]
		else: return rows._mapping
	
	async def run_sql(self, sql):
		async with self.engine.connect() as conn:
			data = await conn.execute(text(sql))

			return data