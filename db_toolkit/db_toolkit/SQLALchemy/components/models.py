from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer
from sqlalchemy.dialects import postgresql 

class Admins:
    def __init__(self, metadata: MetaData) -> None:
        self.name = 'admins'
        self.metadata = metadata

    def get_table(self) -> Table:
        return Table(self.name, self.metadata,
            Column('id', postgresql.INTEGER(), primary_key=True),
            Column('token', postgresql.VARCHAR(32), index=True),
            Column('auth_count', postgresql.SMALLINT()),
            Column('username', postgresql.VARCHAR(50), unique=True),
            Column('password', postgresql.VARCHAR(32)),
        )

def pack_models(metadata: MetaData) -> dict:
    return {
        'admins': Admins(metadata).get_table()
    }