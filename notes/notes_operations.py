"""Functions to operate on notes."""
from __future__ import annotations

from .database import Database
from .note import Note


class Notes:
    """Class to operate on notes."""

    def __init__(self, database_file_name: str = None) -> None:
        self.database = Database(database_file_name)

    def list_notes(self) -> list[Note]:
        """Return a list of notes."""
        return self.database.get_notes()

    def list_note(self, note_id: int) -> Note:
        """Return a note by id."""
        return self.database.get_note_by_id(note_id)

    def new_note(self, **kwargs: dict[str, any]) -> None:
        """Create a new note."""
        note = Note(**kwargs)
        self.database.store_note(note)

    def update_note(self, note_id: int, **kwargs: dict[str, any]) -> None:
        """Update a note."""
        note = self.database.get_note_by_id(note_id)
        note.update(**kwargs)
        self.database.update_note(note)

    def delete_note(self, note_id: int) -> None:
        """Delete a note."""
        note = self.database.get_note_by_id(note_id)
        self.database.delete_note(note)
