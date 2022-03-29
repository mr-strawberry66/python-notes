"""Module to store wrapper around sqlite module."""
import logging
import sqlite3

from .note import Note
from .queries import (
    CREATE_NOTES_TABLE,
    DELETE_NOTE,
    INSERT_NOTE,
    SELECT_MAX_ID,
    SELECT_NOTES,
    SELECT_NOTE_BY_ID,
    UPDATE_NOTE,
)


class SQLite:
    """Context manager for sqlite3 module."""

    def __init__(self, file_name: str = "notes.db") -> None:
        """Initialise the class instance."""
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)

    def __enter__(self):
        """Return the connection object."""
        return self.connection.cursor()

    def __exit__(self, *args):
        """Commit changes and close the connection."""
        self.connection.commit()
        self.connection.close()


class Database:
    """Operate on the database."""

    def __init__(self, database_file_name: str) -> None:
        """Initialise the class instance."""
        self.file_name = database_file_name
        self.create_database()

    def create_database(self) -> None:
        """Create a new database."""
        with SQLite(self.file_name) as cursor:
            try:
                cursor.execute(CREATE_NOTES_TABLE)
            except sqlite3.OperationalError:
                logging.log(logging.INFO, "Database already exists.")

    def get_notes(self) -> None:
        """Return a list of notes."""
        with SQLite(self.file_name) as cursor:
            cursor.execute(SELECT_NOTES)
            return [Note.from_tuple(note) for note in cursor.fetchall()]

    def get_note_by_id(self, _id: int) -> Note:
        """Return a note by id."""
        with SQLite(self.file_name) as cursor:
            cursor.execute(
                SELECT_NOTE_BY_ID,
                (_id,),
            )
            raw = cursor.fetchone()
            if raw:
                return Note.from_tuple(raw)

    def get_highest_id(self) -> int:
        """Return the highest id."""
        with SQLite(self.file_name) as cursor:
            cursor.execute(SELECT_MAX_ID)
            return cursor.fetchone()[0] or 0

    def store_note(self, note: Note) -> None:
        """Store a note in the database."""
        with SQLite(self.file_name) as cursor:
            cursor.execute(
                INSERT_NOTE,
                note.as_tuple(),
            )

    def update_note(self, note: Note) -> None:
        """Update a note."""
        with SQLite(self.file_name) as cursor:
            cursor.execute(
                UPDATE_NOTE,
                note.format_to_update(),
            )

    def delete_note(self, note: Note) -> None:
        """Delete a note."""
        with SQLite(self.file_name) as cursor:
            cursor.execute(
                DELETE_NOTE,
                (note.id_,),
            )
