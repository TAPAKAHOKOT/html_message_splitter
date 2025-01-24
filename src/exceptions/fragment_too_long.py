class FragmentTooLongError(Exception):
    """
    Custom exception raised when a message fragment
    impossible to split with the allowed maximum length.

    Attributes:
        fragment_length (int): The length of the message fragment that
        caused the exception.
        max_length (int): The maximum allowed length for a message fragment.
        message (str): An optional error message describing the exception.
    """

    def __init__(self, fragment_length, max_length, message=None):
        if message is None:
            message = (
                f"Unable to split the message. "
                f"Fragment length ({fragment_length}) "
                f"exceeds the maximum allowed length ({max_length})."
            )
        super().__init__(message)
