from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as mock_connection_handler:
            mock_connection_handler.return_value = True
            call_command('wait_for_db')
            self.assertEqual(mock_connection_handler.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, mock_sleep):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as mock_connection_handler:
            mock_connection_handler.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(mock_connection_handler.call_count, 6)
