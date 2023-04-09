from .components.tables.admins import Admins
from .components.databases import *

database = Database()
admins = Admins(database=database)