from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    year: Mapped[int]
    language: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    # relationships
    author: "Mapped[Author]" = relationship(back_populates="books")
    categories: "Mapped[list[Category]]" = relationship(
        back_populates="books", secondary="books_categories"
    )
    loans: "Mapped[list[Loan]]" = relationship(back_populates="book")
    copies: "Mapped[list[BookCopy]]" = relationship(back_populates="book")  # Agregado


class BookCopy(Base):
    __tablename__ = "book_copies"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    is_available: Mapped[bool] = mapped_column(default=True)

    # relationships
    book: "Mapped[Book]" = relationship(back_populates="copies")

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    biography: Mapped[Optional[str]]
    date_of_birth: Mapped[Optional[date]]

    # relationships
    books: "Mapped[list[Book]]" = relationship(back_populates="author")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # relationships
    books: "Mapped[list[Book]]" = relationship(
        back_populates="categories", secondary="books_categories"
    )


class BookCategory(Base):
    __tablename__ = "books_categories"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)

    loans: "Mapped[list[Loan]]" = relationship(back_populates="client")

class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    loan_date: Mapped[date]
    return_date: Mapped[Optional[date]]
    is_returned: Mapped[bool]
    overdue_fine: Mapped[int] = mapped_column(default=0)  # Nuevo campo para almacenar la multa

    # relationships
    book: "Mapped[Book]" = relationship(back_populates="loans")
    client: "Mapped[Client]" = relationship(back_populates="loans")