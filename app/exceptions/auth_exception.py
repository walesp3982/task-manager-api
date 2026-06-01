class AuthorizationExpired(Exception):
    def __init__(self):
        super().__init__("Authorization expired")


class InvalidCredencials(Exception):
    def __init__(self):
        super().__init__("Invalid Credencials error")
