from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any, Type

from pydantic import BaseModel
from sqlmodel import Session, select

from vovo.utils.orm import get_primary_keys

T = TypeVar("T", bound=BaseModel)


class GenericRepository(Generic[T], ABC):
    """Generic base repository."""

    @abstractmethod
    def get(self, *args: Any, **kwargs: Any) -> Optional[T]:
        """Get a single record by either positional or keyword arguments (or both).

        Args:
            *args (Any): Positional arguments representing values for filtering.
                         The order of arguments should match the expected field order.
            **kwargs (Any): Keyword arguments representing field names and their corresponding values
                            for filtering (e.g., id=1, name="John").

        Returns:
            Optional[T]: Record or None if not found.
        """
        raise NotImplementedError()

    @abstractmethod
    def list(self, limit: int = 100, **filters) -> List[T]:
        """Gets a list of records

        Args:
            limit (int): The maximum number of records to return. Default is 100.
            **filters: Filter conditions, several criteria are linked with a logical 'and'.

         Raises:
            ValueError: Invalid filter condition.

        Returns:
            List[T]: List of records.
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, record: T) -> T:
        """Creates a new record.

        Args:
            record (T): The record to be created.

        Returns:
            T: The created record.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, record: T) -> T:
        """Updates an existing record.

        Args:
            record (T): The record to be updated incl. record id.

        Returns:
            T: The updated record.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, *args: Any, **kwargs: Any) -> None:
        """Deletes a record by either positional or keyword arguments.

        Args:
            *args (Any): Positional arguments representing values for filtering.
            **kwargs (Any): Keyword arguments representing field names and their corresponding values for filtering.
        """
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T], ABC):

    def __init__(self, session: Session, model: Type[T]) -> None:
        """Creates a new repository instance.

        Args:
            session (Session): SQLModel session.
            model (Type[T]): SQLModel class type.
        """
        self.session = session
        self.model = model

    def get(self, *args: Any, **kwargs: Any) -> Optional[T]:

        if args:
            primary_keys = get_primary_keys(self.model)
            if len(args) != len(primary_keys):
                raise ValueError(f"Expected {len(primary_keys)} primary key values, got {len(args)}.")

            # Build a dictionary mapping primary key columns to values
            pk_filter = dict(zip(primary_keys, args))
            query = select(self.model).filter_by(**pk_filter)
        elif kwargs:
            query = select(self.model).filter_by(**kwargs)
        else:
            raise ValueError(
                "Either primary key arguments (*args) or filtering conditions (**kwargs) must be provided.")

        result = self.session.exec(query).first()

        return result

    def list(self, limit: int = 100, **filters) -> List[T]:
        """Gets a list of records from the database."""
        query = select(self.model)
        # Apply filters dynamically
        if filters:
            try:
                query = query.filter_by(**filters)
            except AttributeError as e:
                raise ValueError(f"Invalid filter condition: {e}")

            # Apply limit
        query = query.limit(limit)
        result = self.session.exec(query).all()

        return [self.model(**dict(row)) for row in result]

    def add(self, record: T) -> T:
        """Adds a new record to the database."""
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def update(self, record: T) -> T:
        """Updates an existing record in the database."""
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def delete(self, *args: Any, **kwargs: Any) -> None:
        """Deletes a record from the database using its key."""
        record = self.get(*args, **kwargs)
        if record:
            self.session.delete(record)
            self.session.commit()



