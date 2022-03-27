"""Store queries used for the database."""

CREATE_NOTES_TABLE = """
    CREATE TABLE notes (
        id INTEGER PRIMARY KEY,
        created_at INTEGER,
        category TEXT,
        title TEXT,
        content TEXT,
        tags TEXT,
        due_date TEXT,
        reminder_date TEXT,
        completed INTEGER,
        archived INTEGER,
        deleted INTEGER
    );
"""

SELECT_NOTES = """
    SELECT
        *
    FROM notes
"""

SELECT_NOTE_BY_ID = """
    SELECT
        *
    FROM notes
    WHERE id=?
"""

SELECT_MAX_ID = """
    SELECT
        MAX(id)
    FROM notes
"""

INSERT_NOTE = """
    INSERT INTO notes (
        id,
        created_at,
        category,
        title,
        content,
        tags,
        due_date,
        reminder_date,
        completed,
        archived,
        deleted
    )
    VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
"""

DELETE_NOTE = """
    DELETE FROM notes
    WHERE id=?
"""

UPDATE_NOTE = """
    UPDATE notes
    SET created_at=?,
        category=?,
        title=?,
        content=?,
        tags=?,
        due_date=?,
        reminder_date=?,
        completed=?,
        archived=?,
        deleted=?
    WHERE id=?
"""
