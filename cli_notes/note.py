"""Class to represent one note."""
from __future__ import annotations

from dataclasses import astuple, dataclass


@dataclass
class Note:  # pylint: disable=R0902
    """Class to store a note."""

    id_: int
    created_at: int
    category: str
    title: str
    content: str
    tags: list[str]
    due_date: str
    reminder_date: str
    completed: int
    archived: int
    deleted: int

    def delete(self) -> None:
        """Delete the note."""
        self.deleted = True

    def archive(self) -> None:
        """Archive the note."""
        self.archived = True

    def complete(self) -> None:
        """Mark the note as completed."""
        self.completed = True

    def _join_tags(self) -> str:
        """Join the tags with a comma."""
        self.tags = ", ".join(self.tags)

    def as_tuple(self) -> tuple[int, ...]:
        """Return the note as a tuple."""
        self._join_tags()
        return astuple(self)

    def format_to_update(self) -> tuple[int, ...]:
        """Format the note to update the database correctly."""
        self._join_tags()
        return (
            self.created_at,
            self.category,
            self.title,
            self.content,
            self.tags,
            self.due_date,
            self.reminder_date,
            self.completed,
            self.archived,
            self.deleted,
            self.id_,
        )

    @staticmethod
    def from_tuple(note) -> Note:
        """Return a note from a tuple."""
        return Note(
            id_=note[0],
            created_at=note[1],
            category=note[2],
            title=note[3],
            content=note[4],
            tags=note[5].split(", "),
            due_date=note[6],
            reminder_date=note[7],
            completed=note[8],
            archived=note[9],
            deleted=note[10],
        )
