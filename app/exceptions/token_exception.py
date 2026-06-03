class TokenNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Token not found")


class TokenExpired(Exception):
    def __init__(self) -> None:
        super().__init__("Token expired")
