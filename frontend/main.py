import time
from datetime import datetime

import dearpygui.dearpygui as dpg

from notes_backend import Notes, Note

INDENT_SIZE = 15
NOTES = Notes()

note_dict = {}


def save_note(sender, app_data, user_data):
    """Save a note to the database."""
    if not note_dict.get("id_", None):
        note_dict["id_"] = NOTES.database.get_highest_id() + 1
    if not note_dict.get("created_at", None):
        note_dict["created_at"] = int(time.time())
    if not note_dict.get("completed", None):
        note_dict["completed"] = False
    if not note_dict.get("archived", None):
        note_dict["archived"] = False
    if not note_dict.get("deleted", None):
        note_dict["deleted"] = False
    note_dict["reminder_date"] = None

    note = Note(**note_dict)
    if not NOTES.list_note(note.id_):
        NOTES.database.store_note(note)
    else:
        NOTES.update_note(note.id_, **note_dict)


def regular_text_callback(sender, app_data, user_data):
    note_dict[user_data] = app_data.strip()


def lower_text_callback(sender, app_data, user_data):
    note_dict[user_data] = app_data.lower().strip()


def tags_callback(sender, app_data, user_data):
    note_dict[user_data] = [tag.strip().lower() for tag in app_data.split(",")]


def date_callback(sender, app_data, user_data):
    if app_data["year"] > 99:
        year = app_data["year"] - 100 + 2000
    else:
        year = app_data["year"] + 1900
    date_str = f'{app_data["month_day"]}/{app_data["month"] + 1}/{year}'
    date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    note_dict[user_data] = date


dpg.create_context()
dpg.create_viewport(title="Notes", width=2140, height=2140)
dpg.setup_dearpygui()


def main_window():
    with dpg.window(tag="Main Window", label="Home", width=600, height=1000):
        main_menu = dpg.add_menu_bar(label="Main Menu")
        file_nav = dpg.add_menu(label="File", parent=main_menu)
        dpg.add_menu_item(label="New Note", callback=new_note_window, parent=file_nav)
        dpg.add_menu_item(label="Exit", parent=file_nav)

        dpg.add_listbox(
            items=[
                f"{datetime.fromtimestamp(note.created_at).strftime('%Y-%m-%d')}: {note.title}"
                for note in NOTES.list_notes()
            ],
            label="Notes",
        )


def new_note_window():
    with dpg.window(label="New Note", width=600, height=1000):
        main_menu = dpg.add_menu_bar(label="Main Menu")
        file_nav = dpg.add_menu(label="File", parent=main_menu)
        dpg.add_menu_item(label="Save", callback=save_note, parent=file_nav)

        dpg.add_input_text(
            label="Title",
            width=420,
            multiline=False,
            callback=regular_text_callback,
            user_data="title",
            indent=INDENT_SIZE,
        )

        dpg.add_input_text(
            label="Content",
            width=420,
            multiline=True,
            callback=regular_text_callback,
            user_data="content",
            indent=INDENT_SIZE,
        )

        dpg.add_input_text(
            label="Category",
            width=420,
            multiline=False,
            callback=regular_text_callback,
            user_data="category",
            indent=INDENT_SIZE,
        )

        dpg.add_input_text(
            label="Tags",
            width=420,
            multiline=False,
            callback=tags_callback,
            user_data="tags",
            indent=INDENT_SIZE,
        )

        dpg.add_date_picker(
            label="Due Date",
            user_data="due_date",
            callback=date_callback,
            default_value={"month_day": 29, "month": 3, "year": 22},
            indent=INDENT_SIZE,
        )

        dpg.add_button(
            label="Save",
            callback=save_note,
            width=420,
            indent=INDENT_SIZE,
        )


main_window()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
