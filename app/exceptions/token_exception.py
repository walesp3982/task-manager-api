class TokenNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Token not found")
