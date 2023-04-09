from ..databases import *
from uuid import uuid4

class Admins:
	def __init__(self, database: Database) -> None:
		self.table = database.admins
		self.db = database
	
	async def add(self, username: str):
		async with self.db.engine.connect() as conn:
			data = await conn.execute(
				insert(self.table).values(
					username=username,
					token=uuid4().hex
				).returning(self.table)
			)

			await conn.commit()

			return data.fetchone()
	
	async def get_one_by_id(self, row_id: int):
		async with self.db.engine.connect() as conn:
			data = await conn.execute(
				select(self.table).where(
					self.table.c.id == row_id
				)
			)

			return data.fetchone()
	
	async def get_many_by_id(self, row_ids: List[int]):
		async with self.db.engine.connect() as conn:
			data = await conn.execute(
				select(self.table).where(
					self.table.c.id.in_(row_ids)
				)
			)

			return data.fetchall()
	
	async def check_token(self, token: str):
		async with self.db.engine.connect() as conn:
			data = await conn.execute(
				select(self.table).where(
					self.table.c.token == token
				)
			)

			return data.fetchone()
	
	async def get_all(self):
		async with self.db.engine.connect() as conn:
			data = await conn.execute(
				select(self.table)
			)

			return data.fetchall()

	async def set_field(self, row_id: int, fields: Dict[str, Any]):
		async with self.db.engine.connect() as conn:
			data = await conn.execute(
				update(self.table).where(
					self.table.c.id == row_id
				).values(
					fields
				).returning(self.table)
			)

			await conn.commit()

			return data.fetchone()

	async def delete(self, row_ids: List[int]):
		async with self.db.engine.connect() as conn:
			data = await conn.execute(
				delete(self.table).where(
					self.table.c.id.in_(row_ids)
				).returning(self.table)
			)

			await conn.commit()

			return data.fetchall()
	
	async def auth(self, username: str, password: str):
		update_password = False
		admin = None

		async with self.db.engine.connect() as conn:
			# check if its a first login and set the password
			data = await conn.execute(
				select(self.table).where(
					self.table.c.username == username
				)
			)

			admin = data.fetchone()

			if admin:
				if not admin['password']:
					update_password = True
			
			if not update_password:
				data = await conn.execute(
					select(self.table).where(
						(self.table.c.username == username)
						& (self.table.c.password == password)
						& (self.table.c.auth_count > 0)
					)
				)

				admin = data.fetchone()
			
				return admin
		
		if update_password and admin:
			await self.set_field(admin.id, {'password': password})
			return admin

	async def register_auth_try(self, username: str): 
		async with self.db.engine.connect() as conn:
			await conn.execute(
				update(self.table).where(
					self.table.c.username == username
				).values(
					auth_count=self.table.c.auth_count - 1
				)
			)

			await conn.commit()
		