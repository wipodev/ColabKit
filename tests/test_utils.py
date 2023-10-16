from unittest.mock import patch, MagicMock
from src.ColabKit import utils
import unittest
import os


class UtilsTestCase(unittest.TestCase):

    file_path = "tests/file.txt"
    file_not_exists = "non_existing/file.txt"
    # Create a new file
    with open(f"./{file_path}", 'w') as file:
        pass

    def test_existing_file(self):
        # Test case for an existing file
        result = utils.file_exists(self.file_path)
        self.assertTrue(result)

    def test_non_existing_file(self):
        # Test case for a non-existing file
        result = utils.file_exists(self.file_not_exists)
        self.assertFalse(result)

    def test_directory(self):
        # Test case for a directory
        route = "/tests"
        result = utils.file_exists(route)
        self.assertFalse(result)

    def test_remove_existing_file(self):
        utils.remove_file(self.file_path)
        self.assertFalse(os.path.exists(self.file_path))

    def test_remove_non_existing_file(self):
        # Test removing a non-existing file
        utils.remove_file(self.file_not_exists)
        self.assertFalse(os.path.exists(self.file_not_exists))

    @patch('os.path.exists', side_effect=[False, True, True, True])
    @patch('os.path.getsize', side_effect=[0, 100, 100, 100])
    @patch('time.sleep', new_callable=MagicMock)
    def test_wait_for_existing_unchanged_file(self, mock_sleep, mock_getsize, mock_exists):
        # Test case for an existing file
        result = utils.wait_for_file('test_file.txt', time_limit=3)
        # Assert that the result is True
        self.assertTrue(result)

    @patch('os.path.exists', side_effect=[False, True, True, True])
    @patch('os.path.getsize', side_effect=[0, 100, 200, 200])
    @patch('time.sleep', new_callable=MagicMock)
    def test_wait_for_existing_changed_file(self, mock_sleep, mock_getsize, mock_exists):
        # Test case for an existing file
        result = utils.wait_for_file('test_file.txt', time_limit=3)
        # Assert that the result is True
        self.assertTrue(result)

    @patch('os.path.exists', return_value=False)
    @patch('time.sleep', new_callable=MagicMock)
    def test_wait_for_non_existing_file(self, mock_sleep, mock_exists):
        # Test case for a non-existing file
        result = utils.wait_for_file('non_existing_file.txt', time_limit=3)
        # Assert that the result is False
        self.assertFalse(result)

    @patch('os.path.exists', side_effect=[False, True, True, True])
    @patch('os.path.getsize', side_effect=[0, 100, 100, 100])
    @patch('time.sleep', new_callable=MagicMock)
    def test_wait_for_existing_unchanged_file_with_custom_time_limit(self, mock_sleep, mock_getsize, mock_exists):
        # Test case for an existing file
        result = utils.wait_for_file('test_file.txt', time_limit=2)
        # Assert that the result is True
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
