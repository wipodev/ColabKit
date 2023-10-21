import unittest
from unittest.mock import patch, MagicMock
from src.ColabKit import media
import ffmpeg


class MediaTestCase(unittest.TestCase):

    @patch('src.ColabKit.media.ffmpeg.probe')
    def test_get_duration_valid(self, mock_probe):
        # Configura el retorno simulado de la función ffmpeg.probe
        mock_probe.return_value = {'format': {'duration': '10.5'}}
        video_file = 'video.mp4'
        duration = media.get_duration(video_file)
        self.assertIsInstance(duration, float)
        self.assertEqual(duration, 10.5)

    @patch('src.ColabKit.media.ffmpeg.probe')
    def test_get_video_resolution_valid(self, mock_probe):
        # Configura el retorno simulado de la función ffmpeg.probe
        mock_probe.return_value = {'streams': [
            {'codec_type': 'video', 'width': 1920, 'height': 1080}]}
        video_file = 'video.mp4'
        resolution = media.get_video_resolution(video_file)
        self.assertIsInstance(resolution, tuple)
        self.assertEqual(resolution, (1920, 1080))

    def test_formatted_err(self):
        # Test case for an error message from FFmpeg
        stderr_output = b"Error: Something went wrong\nAnother comment occurred"
        formatted_output = media.get_formatted_error(stderr_output)
        expected_output = "\033[43m\033[101mError: Something went wrong\033[0m"
        # Assert that the error message is correct after formatting
        self.assertEqual(formatted_output, expected_output)

    @patch('ffmpeg.run')
    @patch('builtins.print')
    @patch('src.ColabKit.media.remove_file')
    def test_run_proc_success(self, mock_remove_file, mock_print, mock_run):
        # Test case for a successful FFmpeg process
        mock_run.return_value = None
        result = media.run_process('output_stream', 'output_file', 'message')
        # Assert that the function returned True after executing the FFmpeg process
        self.assertTrue(result)
        # Assert that the print function was called with the expected message
        mock_print.assert_called_with('File message and saved as output_file')
        # Assert that the remove_file function was not called
        mock_remove_file.assert_not_called()

    @patch('ffmpeg.run', side_effect=ffmpeg.Error("", "", stderr=b'Error occurred'))
    @patch('builtins.print')
    @patch('src.ColabKit.media.remove_file')
    def test_run_proc_failure(self, mock_remove_file, mock_print, mock_run):
        # Test case for a failed FFmpeg process
        result = media.run_process('output_stream', 'output_file', 'message')
        # Assert that the function returned False after executing the FFmpeg process
        self.assertFalse(result)
        # Assert that the print function was called with the expected message
        mock_print.assert_called_with(
            media.get_formatted_error(b'Error occurred'))
        # Assert that the remove_file function was called
        mock_remove_file.assert_called_with('output_file')

    @patch('src.ColabKit.media.run_process', return_value=True)
    @patch('builtins.print')
    def test_conv_success(self, mock_print, mock_run_process):
        # Test case for a successful conversion
        result = media.convert('input_file.mp4', 'output_file.mp4')
        # Assert that the function returned True after executing the FFmpeg process
        mock_print.assert_called_with(
            "Converting input_file.mp4 to output_file.mp4...")
        # Assert that the remove_file function was called
        self.assertTrue(result)

    @patch('src.ColabKit.media.run_process', return_value=False)
    @patch('builtins.print')
    def test_conv_failure(self, mock_print, mock_run_process):
        # Test case for a failed conversion
        result = media.convert('input_file.mp4', 'output_file.mp4')
        # Assert that the function returned False after executing the FFmpeg process
        mock_print.assert_called_with(
            "Converting input_file.mp4 to output_file.mp4...")
        # Assert that the remove_file function was called
        self.assertFalse(result)

    @patch('src.ColabKit.media.run_process', return_value=True)
    @patch('builtins.print')
    def test_short_success(self, mock_print, mock_run_process):
        # Test case for a successful trim
        result = media.shorten('input_file.mp4', 10, 5, 'output_file.mp4')
        # Assert that the function returned True after executing the FFmpeg process
        mock_print.assert_called_with(
            "shorting input_file.mp4 to 5 seconds...")
        # Assert that the remove_file function was called
        self.assertTrue(result)

    @patch('src.ColabKit.media.run_process', return_value=False)
    @patch('builtins.print')
    def test_short_failure(self, mock_print, mock_run_process):
        # Test case for a failed trim
        result = media.shorten('input_file.mp4', 10, 5, 'output_file.mp4')
        # Assert that the function returned False after executing the FFmpeg process
        mock_print.assert_called_with(
            "shorting input_file.mp4 to 5 seconds...")
        # Assert that the remove_file function was called
        self.assertFalse(result)

    @patch('src.ColabKit.media.get_video_resolution', return_value=(1920, 1080))
    @patch('src.ColabKit.media.run_process', return_value=True)
    @patch('builtins.print')
    def test_resize_video_success(self, mock_print, mock_run_process, mock_get_video_resolution):
        # Test case for a successful resize
        result = media.resize_video('input_video.mp4', 720)
        # Assert that the function returned True after executing the FFmpeg process
        mock_print.assert_called_with("Resizing video to 720p...")
        # Assert that the remove_file function was called
        self.assertEqual(result, 'input_video_720p.mp4')

    @patch('src.ColabKit.media.get_video_resolution', return_value=(1280, 720))
    @patch('src.ColabKit.media.run_process', return_value=True)
    @patch('builtins.print')
    def test_resize_video_small_resolution(self, mock_print, mock_run_process, mock_get_video_resolution):
        # Test case for a successful resize
        result = media.resize_video('input_video.mp4', 720)
        # Assert that the function returned True after executing the FFmpeg process
        mock_print.assert_called_with("No need to change the size")
        # Assert that the remove_file function was called
        self.assertEqual(result, 'input_video.mp4')

    @patch('src.ColabKit.media.get_video_resolution', return_value=(640, 360))
    @patch('builtins.print')
    def test_resize_video_no_need_to_change(self, mock_print, mock_get_video_resolution):
        # Test case for a successful resize
        result = media.resize_video('input_video.mp4', 720)
        # Assert that the function returned True after executing the FFmpeg process
        mock_print.assert_called_with("No need to change the size")
        # Assert that the remove_file function was called
        self.assertEqual(result, 'input_video.mp4')
        # Assert that the get_video_resolution function was called
        mock_get_video_resolution.assert_called_once_with('input_video.mp4')

    @patch('src.ColabKit.media.get_video_resolution', return_value=(1920, 1080))
    @patch('src.ColabKit.media.run_process', return_value=False)
    @patch('builtins.print')
    def test_resize_video_failure(self, mock_print, mock_run_process, mock_get_video_resolution):
        # Test case for a failed resize
        result = media.resize_video('input_video.mp4', 720)
        # Assert that the function returned False after executing the FFmpeg process
        mock_print.assert_called_with("Resizing video to 720p...")
        # Assert that the remove_file function was called
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
