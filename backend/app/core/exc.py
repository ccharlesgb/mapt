class DatasetNotFoundError(Exception):
    """
    Raised when a Dataset is requested but it does not exist in the DB
    """
