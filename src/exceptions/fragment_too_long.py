class FragmentTooLongError(Exception):
    def __init__(self, fragment_length, max_length, message=None):
        if message is None:
            message = (
                f"Unable to split the message. "
                f"Fragment length ({fragment_length}) "
                f"exceeds the maximum allowed length ({max_length})."
            )
        super().__init__(message)
