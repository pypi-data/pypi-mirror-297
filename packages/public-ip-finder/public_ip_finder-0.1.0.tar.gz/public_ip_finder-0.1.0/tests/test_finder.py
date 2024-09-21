import unittest
from public_ip_finder.finder import get_public_ip

class TestPublicIPFinder(unittest.TestCase):
    def test_get_public_ip(self):
        ip = get_public_ip()
        self.assertIsNotNone(ip)
        self.assertIsInstance(ip, str)

if __name__ == '__main__':
    unittest.main()