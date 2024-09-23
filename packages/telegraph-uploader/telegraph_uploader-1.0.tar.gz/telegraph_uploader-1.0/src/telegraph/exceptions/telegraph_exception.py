class TelegraphException(Exception):
    """
    Custom exception class for handling errors from the Telegraph API.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Telegraph API Error: {self.message}"