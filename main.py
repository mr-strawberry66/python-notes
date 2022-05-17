import time
from datetime import datetime

import dearpygui.dearpygui as dpg

from notes_backend import Notes, Note

from screeninfo import get_monitors


screen = get_monitors()[0]

WIDTH = screen.width // 2
HEIGHT = screen.height // 2

INDENT_SIZE = 15
NOTES = Notes()

note_dict = {}

dpg.create_context()
vp = dpg.create_viewport(title="Notes", width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()

WIDGET_WIDTH = dpg.get_viewport_width() // 1.5


def current_date():
    """Return the current date formatted for DearPyGui."""
    today = datetime.now()
    year = today.year - 2000 + 100
    return {
        "month_day": today.day,
        "month": today.month - 1,
        "year": year,
    }


def reset_note_dict():
    note_dict.clear()


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
    main_window()
    dpg.hide_item(user_data)
    reset_note_dict()


def cancel_new_note(sender, app_data, user_data):
    main_window()
    dpg.delete_item(user_data)
    reset_note_dict()


def delete_note(sender, app_data, user_data):
    """Delete a note from the database."""
    user_data = tuple(user_data)
    note_id = user_data[0]
    window = user_data[1]
    NOTES.update_note(note_id, **{"deleted": True})
    dpg.hide_item(window)
    reset_note_dict()
    main_window()


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


def edit_note(sender, app_data, user_data):
    """Open a note from the database."""
    dpg.delete_item("Main Window")
    note_id = app_data.split(":")[0].strip()
    note = NOTES.list_note(note_id)

    note_dict["id_"] = note.id_
    note_dict["title"] = note.title
    note_dict["content"] = note.content
    note_dict["category"] = note.category
    note_dict["tags"] = note.tags
    note_dict["due_date"] = note.due_date

    with dpg.window(
        label=f"Edit {note.title}",
        width=WIDTH,
        height=HEIGHT,
        pos=[0, 0],
        on_close=cancel_new_note,
        user_data="Main Menu",
    ) as window:
        main_menu = dpg.add_menu_bar(label="Main Menu")
        file_nav = dpg.add_menu(label="File", parent=main_menu)
        dpg.add_menu_item(
            label="Save",
            callback=save_note,
            parent=file_nav,
            user_data=window,
        )
        dpg.add_menu_item(
            label="Cancel",
            callback=cancel_new_note,
            parent=file_nav,
            user_data=window,
        )

        dpg.add_input_text(
            label="Title",
            width=WIDGET_WIDTH,
            multiline=False,
            callback=regular_text_callback,
            user_data="title",
            indent=INDENT_SIZE,
            default_value=note.title,
        )

        dpg.add_input_text(
            label="Content",
            width=WIDGET_WIDTH,
            multiline=True,
            callback=regular_text_callback,
            user_data="content",
            indent=INDENT_SIZE,
            default_value=note.content,
        )

        dpg.add_input_text(
            label="Category",
            width=WIDGET_WIDTH,
            multiline=False,
            callback=regular_text_callback,
            user_data="category",
            indent=INDENT_SIZE,
            default_value=note.category,
        )

        dpg.add_input_text(
            label="Tags",
            width=WIDGET_WIDTH,
            multiline=False,
            callback=tags_callback,
            user_data="tags",
            indent=INDENT_SIZE,
            default_value=", ".join(note.tags),
        )

        dpg.add_date_picker(
            label="Due Date",
            user_data="due_date",
            callback=date_callback,
            default_value=current_date(),
            indent=INDENT_SIZE,
        )
        dpg.add_button(
            label="Save",
            callback=save_note,
            width=WIDGET_WIDTH,
            indent=INDENT_SIZE,
            user_data=window,
        )
        dpg.add_button(
            label="Delete Note",
            callback=delete_note,
            width=WIDGET_WIDTH,
            indent=INDENT_SIZE,
            user_data=(note.id_, window),
        )
        dpg.add_button(
            label="Cancel",
            callback=cancel_new_note,
            width=WIDGET_WIDTH,
            indent=INDENT_SIZE,
            user_data=window,
        )


def main_window():
    with dpg.window(
        tag="Main Window",
        label="Home",
        width=WIDTH,
        height=HEIGHT,
        on_close=dpg.stop_dearpygui,
    ) as window:

        main_menu = dpg.add_menu_bar(label="Main Menu")
        file_nav = dpg.add_menu(label="File", parent=main_menu)
        dpg.add_menu_item(label="New Note", callback=new_note_window, parent=file_nav)
        dpg.add_menu_item(label="Exit", parent=file_nav, callback=dpg.stop_dearpygui)

        dpg.add_listbox(
            items=sorted(
                [note for note in NOTES.list_notes() if not note.deleted],
                reverse=True,
            ),
            label="Notes",
            width=WIDGET_WIDTH,
            callback=edit_note,
            indent=INDENT_SIZE,
        )

        dpg.add_button(
            label="New Note",
            callback=new_note_window,
            width=WIDGET_WIDTH,
            indent=INDENT_SIZE,
        )
        dpg.add_button(
            label="Exit",
            callback=dpg.stop_dearpygui,
            width=WIDGET_WIDTH,
            indent=INDENT_SIZE,
        )


def new_note_window():
    dpg.delete_item("Main Window")
    with dpg.window(
        label="New Note",
        width=WIDTH,
        height=HEIGHT,
        on_close=cancel_new_note,
        user_data="Main Menu",
    ) as window:
        main_menu = dpg.add_menu_bar(label="Main Menu")
        file_nav = dpg.add_menu(label="File", parent=main_menu)
        dpg.add_menu_item(
            label="Save",
            callback=save_note,
            parent=file_nav,
            user_data=window,
        )
        dpg.add_menu_item(
            label="Cancel",
            callback=cancel_new_note,
            parent=file_nav,
            user_data=window,
        )

        dpg.add_input_text(
            label="Title",
            width=WIDGET_WIDTH,
            multiline=False,
            callback=regular_text_callback,
            user_data="title",
            indent=INDENT_SIZE,
        )

        dpg.add_input_text(
            label="Content",
            width=WIDGET_WIDTH,
            multiline=True,
            callback=regular_text_callback,
            user_data="content",
            indent=INDENT_SIZE,
        )

        dpg.add_input_text(
            label="Category",
            width=WIDGET_WIDTH,
            multiline=False,
            callback=regular_text_callback,
            user_data="category",
            indent=INDENT_SIZE,
        )

        dpg.add_input_text(
            label="Tags",
            width=WIDGET_WIDTH,
            multiline=False,
            callback=tags_callback,
            user_data="tags",
            indent=INDENT_SIZE,
        )

        dpg.add_date_picker(
            label="Due Date",
            user_data="due_date",
            callback=date_callback,
            default_value=current_date(),
            indent=INDENT_SIZE,
        )

        dpg.add_button(
            label="Save",
            callback=save_note,
            width=WIDGET_WIDTH,
            indent=INDENT_SIZE,
            user_data=window,
        )
        dpg.add_button(
            label="Cancel",
            callback=cancel_new_note,
            width=WIDGET_WIDTH,
            indent=INDENT_SIZE,
            user_data=window,
        )


main_window()

dpg.show_viewport()

while dpg.is_dearpygui_running():
    WIDTH = dpg.get_viewport_width()
    HEIGHT = dpg.get_viewport_height()
    WIDGET_WIDTH = WIDTH // 1.5
    window = dpg.get_active_window()
    if window:
        if dpg.does_item_exist(window):
            if hasattr(window, "width") and hasattr(window, "height"):
                dpg.set_item_width(window, WIDTH)
                dpg.set_item_height(window, HEIGHT)
    dpg.render_dearpygui_frame()

dpg.destroy_context()
