from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Author, Book, Client, Loan, Category


class AuthorReadDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"books"})


class AuthorReadFullDTO(SQLAlchemyDTO[Author]):
    pass


class AuthorWriteDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"})


class AuthorUpdateDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"}, partial=True)


class BookReadDTO(SQLAlchemyDTO[Book]):
    pass


class BookWriteDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"id", "author", "categories.0.name"})


class BookUpdateDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"id", "author"}, partial=True)


class ClientReadDTO(SQLAlchemyDTO[Client]):
    pass


class ClientWriteDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(exclude={"id", "borrowed_books"})


class ClientUpdateDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(exclude={"id", "borrowed_books"}, partial=True)


class LoanReadDTO(SQLAlchemyDTO[Loan]):
    pass

class LoanReadFullDTO(SQLAlchemyDTO[Loan]):
    pass

class LoanWriteDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(exclude={"id", "returned"})

class LoanUpdateDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(exclude={"id"}, partial=True)


class CategoryReadDTO(SQLAlchemyDTO[Category]):
    pass

class CategoryWriteDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id"})

class CategoryUpdateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id"}, partial=True)