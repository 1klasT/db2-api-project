from litestar import Litestar

from app.controlers import AuthorController, BookController, ClientController, LoanController, CategoryController
from app.database import sqlalchemy_config

app = Litestar([AuthorController, BookController, ClientController, LoanController, CategoryController], debug=True, plugins=[sqlalchemy_config])
