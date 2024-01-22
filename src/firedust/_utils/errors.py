class MissingFiredustKeyError(Exception):
    def __init__(self) -> None:
        message = """
        The FIREDUST_API_KEY environment variable is not found. 
        Please, run firedust.connect.cloud(api_key) to set the API key.
        """
        super().__init__(message)


class APIError(Exception):
    def __init__(self, message: str, code: int = 500) -> None:
        self.code = code
        super().__init__(message)

    def __str__(self) -> str:
        return f"APIError (code={self.code}): {super().__str__()}"
