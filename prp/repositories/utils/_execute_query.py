from prp.db import get_db

# TODO: set db as parameter
def _execute_query(query, params=(), commit=False):
    with get_db() as db:
        # TODO: try-except in execution
        cursor = db.cursor()
        cursor.execute(query, params)
        # TODO: erase commit from this method and make it where the connection is made
        if commit:
            db.commit()
        return cursor