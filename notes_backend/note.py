"""Class to represent one note."""
from __future__ import annotations

from dataclasses import astuple, dataclass
from datetime import datetime


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
    completed: bool
    archived: bool
    deleted: bool

    def __repr__(self) -> str:
        """String representation of the note."""
        if self.id_ < 10:
            spacing = "   "
        elif self.id_ >= 10 and self.id_ < 999:
            spacing = "  "
        else:
            spacing = " "
        time = datetime.fromtimestamp(self.created_at).strftime("%Y-%m-%d")
        return f"{self.id_}:{spacing}{time}: {self.title}"

    def __lt__(self, other):
        """Compare the note to another note."""
        return self.created_at < other.created_at

    def delete(self) -> None:
        """Delete the note."""
        self.deleted = True

    def archive(self) -> None:
        """Archive the note."""
        self.archived = True

    def complete(self) -> None:
        """Mark the note as completed."""
        self.completed = True

    def update(self, **kwargs) -> Note:
        """Update the note."""
        for key in self.__dict__.keys():
            if kwargs.get(key, None) is not None:
                setattr(self, key, kwargs[key])

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

    @classmethod
    def from_tuple(cls, note) -> Note:
        """Return a note from a tuple."""
        return cls(
            id_=note[0],
            created_at=note[1],
            category=note[2],
            title=note[3],
            content=note[4],
            tags=note[5].split(", "),
            due_date=note[6],
            reminder_date=note[7],
            completed=bool(note[8]),
            archived=bool(note[9]),
            deleted=bool(note[10]),
        )
