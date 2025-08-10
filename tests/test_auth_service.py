import unittest

from services.auth_service import AuthService


class MockStorage:
    """In-memory storage for testing"""
    def __init__(self):
        self.users = {}

    def load_users(self):
        return dict(self.users)

    def save_user(self, user):
        self.users[user.username] = user.password


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.storage = MockStorage()
        self.service = AuthService(self.storage)

    def test_register_and_login(self):
        self.assertEqual(self.service.register("alice", "password"), "注册成功")
        self.assertTrue(self.service.login("alice", "password"))
        self.assertFalse(self.service.login("alice", "wrong"))

    def test_register_duplicate_user(self):
        self.service.register("bob", "secret")
        with self.assertRaises(ValueError):
            self.service.register("bob", "secret")


if __name__ == "__main__":
    unittest.main()
