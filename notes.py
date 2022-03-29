import click
from commands.notes_commands import list_notes, new_note, delete_note, update


@click.group()
def cli():
    """Group for Notes CLI."""


@cli.command()
def version():
    """Print version."""
    print("0.0.1")


cli.add_command(cmd=list_notes, name="list")
cli.add_command(cmd=new_note, name="new")
cli.add_command(cmd=delete_note, name="delete")
cli.add_command(cmd=update, name="update")
