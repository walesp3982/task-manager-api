class UserNotFound(Exception):
    def __init__(self, msg: str = ""):
        super().__init__("User not found" if msg == "" else msg)


class UserNotFoundById(UserNotFound):
    def __init__(self, id: int):
        super().__init__(f"User by id: {id} not found")


class UserNotFoundByEmail(UserNotFound):
    def __init__(self, email: str):
        super().__init__(f"User by email: {email} not found")
