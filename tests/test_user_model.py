import unittest
from kylereads.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = '123')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_read(self):
        u = User(password = '123')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = '123')
        self.assertTrue(u.verify_password('123'))
        self.assertFalse(u.verify_password('dog'))

    def test_random_hashes(self):
        u = User(password = '123')
        u2 = User(password = '123')
        self.assertTrue(u.password_hash != u2.password_hash)
