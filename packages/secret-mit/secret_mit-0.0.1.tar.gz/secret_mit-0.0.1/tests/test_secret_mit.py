import io
import sys
from unittest import TestCase
from unittest.mock import patch

class TestSecretMit(TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_import_message(self, mock_stdout):
        import secret_mit
        self.assertEqual(mock_stdout.getvalue().strip(), "hello from sundai-club")

