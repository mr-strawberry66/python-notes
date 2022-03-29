import click
from notes_backend import Notes

from .cli_functions import (
    format_note,
    format_notes,
    new_note_as_dict,
    update_note_as_dict,
)

NOTES = Notes()


@click.command(name="list")
@click.option(
    "-i",
    "--id",
    "id_",
    type=int,
    help="ID of the note to display",
    default=lambda: None,
)
def list_notes(id_: int):
    """List notes."""
    if id_ is None:
        for note in NOTES.list_notes():
            print(format_notes(note))
    else:
        print(format_note(NOTES.list_note(id_)))


@click.command(name="new")
def new_note():
    """Create a new note."""
    note = new_note_as_dict()
    NOTES.new_note(**note)


@click.command(name="delete")
@click.option(
    "-i",
    "--id",
    "id_",
    type=int,
    help="ID of the note to delete",
)
def delete_note(id_: int):
    """Delete a note."""
    NOTES.delete_note(id_)


@click.group()
def update():
    """Update existing notes."""


@update.command()
@click.option(
    "-i",
    "--id",
    "id_",
    type=int,
    help="ID of the note to update",
)
def note(id_: int):
    """Update a note."""
    note = NOTES.database.get_note_by_id(id_)
    note_params = update_note_as_dict(note)
    NOTES.update_note(id_, **note_params)


@update.command()
@click.option(
    "-i",
    "--id",
    "id_",
    type=int,
    help="ID of the note to update",
)
def title(id_: int):
    """Update a note's title."""
    note = NOTES.database.get_note_by_id(id_)
    note_params = update_note_as_dict(note)
    NOTES.update_note(id_, **note_params)
