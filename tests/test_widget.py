from unittest.mock import MagicMock, patch
from src.ColabKit.widget import button
import ipywidgets as widgets
import unittest


class WidgetTestCase(unittest.TestCase):

    text = "My Button"
    tip = "Click here"
    style = "success"
    func = MagicMock()
    param = (1, 2, 3)


def test_generate_button_creation(self):
    with patch('ipywidgets.Button', new_callable=MagicMock) as mock_button:
        # Create the button and call the function with the given arguments
        generate_button(self.text, self.tip, self.style,
                        self.func, *self.param)
        # Assert that the Button class was called with the expected arguments
        mock_button.assert_called_with(
            description=self.text, button_style=self.style, tooltip=self.tip, icon="erase")

    def test_generate_button_function_execution(self):
        # Create button with specified parameters
        button = generate_button(
            self.text, self.tip, self.style, self.func, *self.param)
        # Simulate button click
        button.click()
        # Verify that the function was called with the expected parameters
        self.func.assert_called_with(*self.param)


if __name__ == '__main__':
    unittest.main()
