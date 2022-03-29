from __future__ import annotations
from textwrap import dedent
import time
import editor
from datetime import datetime
from notes_backend import Note


def format_notes(note) -> str:
    return dedent(
        f"""
ID: {note.id_}
Category: {note.category}
Title: {note.title}
Due: {note.due_date}
"""
    )


def format_note(note) -> str:
    return dedent(
        f"""
ID: {note.id_}
Category: {note.category}
Title: {note.title}

---

{note.content}

---

Tags: {", ".join(note.tags)}
Due: {note.due_date}

Completed: {note.completed}
"""
    )


def new_note_as_dict() -> dict[str, any]:
    return {
        "created_at": int(time.time()),
        "category": get_category(),
        "title": get_title(),
        "content": get_content(),
        "tags": get_tags(),
        "due_date": get_date("due"),
        "reminder_date": None,
        "completed": False,
        "archived": False,
        "deleted": False,
    }


def update_note_as_dict(note: Note) -> dict[str, any]:
    """Update a note based on user input."""
    return {
        "category": get_category(note),
        "title": get_title(note),
        "content": get_content(note),
        "tags": get_tags(),
        "due_date": get_date("due"),
        "reminder_date": None,
        "completed": True if input("Completed? (y/n): ").lower() == "y" else False,
        "archived": True if input("Archive? (y/n): ").lower() == "y" else False,
        "deleted": True if input("Completed? (y/n): ").lower() == "y" else False,
    }


def get_category(note: Note = None) -> str:
    return input(f"Category: {note.category if note else ''}")


def get_title(note: Note = None) -> str:
    return input(f"Title: {note.title if note else ''}")


def get_tags() -> str:
    return input(f"Tags (seperate by comma): ").lower().split(", ")


def get_content(note: Note = None) -> str:
    while True:
        if not note:
            body = (
                editor.edit(contents="# Replace this text with your note.")
                .decode("utf-8")
                .strip()
            )
            if not body:
                print("\nPlease input content for your note.\n")
                pass
            else:
                return body
        else:
            body = (
                editor.edit(
                    contents=note.content,
                )
                .decode("utf-8")
                .strip()
            )
            return body


def get_date(arg: str) -> str:
    """Set the due / reminder date of a note based on user input."""
    while True:
        date = input(f"Set a {arg} date in yyyy-mm-dd format (optional): ")
        if not date:
            return None
        else:
            try:
                timestamp = datetime.strptime(date, "%Y-%m-%d")
                return timestamp.strftime("%Y-%m-%d")
            except ValueError:
                print(f"Date must be yyyy-mm-dd format\n")
