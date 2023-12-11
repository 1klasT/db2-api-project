from advanced_alchemy.filters import SearchFilter
from litestar import Controller, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from litestar.repository import NotFoundError
from datetime import datetime

from app.dtos import (
    AuthorReadDTO,
    AuthorReadFullDTO,
    AuthorUpdateDTO,
    AuthorWriteDTO,
    BookReadDTO,
    BookUpdateDTO,
    BookWriteDTO,
    ClientReadDTO, 
    ClientUpdateDTO, 
    ClientWriteDTO,
    LoanReadDTO,
    LoanReadFullDTO,
    LoanUpdateDTO,
    LoanWriteDTO,
    CategoryReadDTO, 
    CategoryUpdateDTO, 
    CategoryWriteDTO,
)
from app.models import Author, Client, Book, Loan, Category
from app.repositories import (
    AuthorRepository,
    BookRepository,
    ClientRepository,
    LoanRepository,
    CategoryRepository,
    provide_authors_repo,
    provide_books_repo,
    provide_clients_repo,
    provide_loans_repo,
    provide_categories_repo,
)


class AuthorController(Controller):
    path = "/authors"
    tags = ["authors"]
    return_dto = AuthorReadDTO
    dependencies = {"authors_repo": Provide(provide_authors_repo)}

    @get()
    async def list_authors(self, authors_repo: AuthorRepository) -> list[Author]:
        return authors_repo.list()

    @post(dto=AuthorWriteDTO)
    async def create_author(self, data: Author, authors_repo: AuthorRepository) -> Author:
        return authors_repo.add(data)

    @get("/{author_id:int}", return_dto=AuthorReadFullDTO)
    async def get_author(self, author_id: int, authors_repo: AuthorRepository) -> Author:
        try:
            return authors_repo.get(author_id)
        except NotFoundError as e:
            raise HTTPException(detail="Author not found", status_code=404) from e

    @patch("/{author_id:int}", dto=AuthorUpdateDTO)
    async def update_author(
        self, author_id: int, data: DTOData[Author], authors_repo: AuthorRepository
    ) -> Author:
        try:
            author = authors_repo.get(author_id)
            author = data.update_instance(author)
            return authors_repo.update(author)
        except NotFoundError as e:
            raise HTTPException(detail="Author not found", status_code=404) from e


class BookController(Controller):
    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_books_repo)}

    @get()
    async def list_books(self, books_repo: BookRepository) -> list[Book]:
        return books_repo.list()

    @get("/search")
    async def search_books(self, books_repo: BookRepository, q: str) -> list[Book]:
        return books_repo.list(SearchFilter("title", q))

    @post(dto=BookWriteDTO)
    async def create_book(self, data: DTOData[Book], books_repo: BookRepository, categories_repo: CategoryRepository) -> Book:
        # Verifica si hay categorías seleccionadas
        if not data.categories:
            raise HTTPException(detail="Debe seleccionar al menos una categoría para el libro.", status_code=400)

        # Obtén las instancias de categorías basadas en los ID proporcionados
        selected_categories = categories_repo.get_multiple(data.categories)

        # Asigna las categorías al libro
        book = data.to_instance()
        book.categories = selected_categories

        # Guarda el libro en la base de datos
        return books_repo.add(book)

    @get("/{book_id:int}")
    async def get_book(self, book_id: int, books_repo: BookRepository) -> Book:
        try:
            return books_repo.get(book_id)
        except NotFoundError as e:
            raise HTTPException(detail="Book not found", status_code=404) from e

    @patch("/{book_id:int}", dto=BookUpdateDTO)
    async def update_book(
        self, book_id: int, data: DTOData[Book], books_repo: BookRepository
    ) -> Book:
        try:
            book = books_repo.get(book_id)
            book = data.update_instance(book)
            return books_repo.update(book)
        except NotFoundError as e:
            raise HTTPException(detail="Book not found", status_code=404) from e

class ClientController(Controller):
    path = "/clients"
    tags = ["clients"]
    return_dto = ClientReadDTO
    dependencies = {"clients_repo": Provide(provide_clients_repo)}

    @get()
    async def list_clients(self, clients_repo: ClientRepository) -> list[Client]:
        return clients_repo.list()

    @post(dto=ClientWriteDTO)
    async def create_client(self, data: Client, clients_repo: ClientRepository) -> Client:
        return clients_repo.add(data)

    @get("/{client_id:int}", return_dto=ClientReadDTO)
    async def get_client(self, client_id: int, clients_repo: ClientRepository) -> Client:
        try:
            return clients_repo.get(client_id)
        except NotFoundError as e:
            raise HTTPException(detail="Client not found", status_code=404) from e

    @patch("/{client_id:int}", dto=ClientUpdateDTO)
    async def update_client(
        self, client_id: int, data: DTOData[Client], clients_repo: ClientRepository
    ) -> Client:
        try:
            client = clients_repo.get(client_id)
            client = data.update_instance(client)
            return clients_repo.update(client)
        except NotFoundError as e:
            raise HTTPException(detail="Client not found", status_code=404) from e
        
class LoanController(Controller):
    path = "/loans"
    tags = ["loans"]
    return_dto = LoanReadDTO
    dependencies = {
        "loans_repo": Provide(provide_loans_repo),
        "books_repo": Provide(provide_books_repo)  # Agrega esta línea
    }

    @get()
    async def list_loans(self, loans_repo: LoanRepository) -> list[Loan]:
        return loans_repo.list()

    @post(dto=LoanWriteDTO)
    async def create_loan(
    self, data: Loan, loans_repo: LoanRepository, books_repo: BookRepository) -> Loan:
        book = books_repo.get(data.book_id)

        if not book or book.copies_available <= 0:
            raise HTTPException(
                status_code=400, detail="No es posible realizar el préstamo de este libro."
            )
        
        book.copies_available -= 1
        loans_repo.add(data)

        books_repo.update(book)

        return data

    @get("/{loan_id:int}", return_dto=LoanReadFullDTO)
    async def get_loan(self, loan_id: int, loans_repo: LoanRepository) -> Loan:
        try:
            return loans_repo.get(loan_id)
        except NotFoundError as e:
            raise HTTPException(detail="Loan not found", status_code=404) from e

    @patch("/{loan_id:int}", dto=LoanUpdateDTO)
    async def update_loan(
        self, loan_id: int, data: DTOData[Loan], loans_repo: LoanRepository
    ) -> Loan:
        try:
            loan = loans_repo.get(loan_id)
            loan = data.update_instance(loan)
            return loans_repo.update(loan)
        except NotFoundError as e:
            raise HTTPException(detail="Loan not found", status_code=404) from e
        
    @patch("/{loan_id:int}/return", dto=LoanUpdateDTO)
    async def return_loan(
        self, loan_id: int, data: DTOData[Loan], loans_repo: LoanRepository, books_repo: BookRepository
    ) -> Loan:
        try:
            loan = loans_repo.get(loan_id)

            if loan.is_returned:
                raise HTTPException(status_code=400, detail="El libro ya ha sido devuelto.")

            return_date = data.return_date or datetime.now().date()

            # Calcular la multa si la devolución se realiza después de la fecha límite
            overdue_days = (return_date - loan.loan_date).days
            fine_rate_per_day = 5  # Puedes ajustar esto según tus requisitos
            overdue_fine = max(0, overdue_days - 7) * fine_rate_per_day

            loan.return_date = return_date
            loan.is_returned = True
            loan.overdue_fine = overdue_fine

            # Aumentar las copias disponibles del libro al devolverlo
            book = loan.book
            book.copies_available += 1

            loans_repo.update(loan)
            books_repo.update(book)

            return loan

        except NotFoundError as e:
            raise HTTPException(detail="Préstamo no encontrado", status_code=404) from e

class CategoryController(Controller):
    path = "/categories"
    tags = ["categories"]
    return_dto = CategoryReadDTO
    dependencies = {"categories_repo": Provide(provide_categories_repo)}

    @get()
    async def list_categories(self, categories_repo: CategoryRepository) -> list[Category]:
        return categories_repo.list()

    @post(dto=CategoryWriteDTO)
    async def create_category(self, data: Category, categories_repo: CategoryRepository) -> Category:
        return categories_repo.add(data)

    @get("/{category_id:int}")
    async def get_category(self, category_id: int, categories_repo: CategoryRepository) -> Category:
        try:
            return categories_repo.get(category_id)
        except NotFoundError as e:
            raise HTTPException(detail="Category not found", status_code=404) from e

    @patch("/{category_id:int}", dto=CategoryUpdateDTO)
    async def update_category(
        self, category_id: int, data: DTOData[Category], categories_repo: CategoryRepository
    ) -> Category:
        try:
            category = categories_repo.get(category_id)
            category = data.update_instance(category)
            return categories_repo.update(category)
        except NotFoundError as e:
            raise HTTPException(detail="Category not found", status_code=404) from e