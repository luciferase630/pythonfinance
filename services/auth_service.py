from auth.storage import Storage
from auth.auth_system import AuthSystem


class AuthService:
    """Service layer for authentication to decouple UI from storage"""

    def __init__(self, storage: Storage | None = None) -> None:
        self.storage = storage or Storage()
        self.auth_system = AuthSystem(self.storage)

    def register(self, username: str, password: str) -> str:
        """Register a new user"""
        return self.auth_system.register(username, password)

    def login(self, username: str, password: str) -> bool:
        """Validate user credentials"""
        return self.auth_system.login(username, password)
