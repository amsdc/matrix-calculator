class Error(Exception):
    """A base for all errors.

    Other errors inherit this error.
    """
    pass

class UpdationError(Error):
    """Failure to update data in the Database."""
