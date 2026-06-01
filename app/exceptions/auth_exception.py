class AuthorizationExpired(Exception):
    def __init__(self):
        super().__init__("Authorization expired")
