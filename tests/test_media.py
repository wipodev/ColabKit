import unittest
from unittest.mock import patch, MagicMock
from src.ColabKit import media
import ffmpeg


class MediaTestCase(unittest.TestCase):

    @patch('src.ColabKit.media.VideoFileClip')
    def test_video_duration(self, mock_video_file_clip):
        # Test case for a video file with a duration of 10.5 seconds
        mock_instance = mock_video_file_clip.return_value
        mock_instance.duration = 10.5
        duration = media.video_duration('video_path.mp4')
        # Assert that the duration is correct
        self.assertEqual(duration, 10.5)

    @patch('src.ColabKit.media.VideoFileClip')
    def test_get_video_resolution(self, mock_video_file_clip):
        # Test case for a video file with a resolution of 1920x1080
        mock_instance = mock_video_file_clip.return_value
        mock_instance.size = (1920, 1080)
        resolution = media.get_video_resolution('video_path.mp4')
        # Assert that the resolution is correct
        self.assertEqual(resolution, (1920, 1080))

    def test_ffmpeg_err(self):
        # Test case for an error message from FFmpeg
        stderr_output = b"Error: Something went wrong\nAnother comment occurred"
        formatted_output = media.ffmpeg_err(stderr_output)
        expected_output = "\033[43m\033[101mError: Something went wrong\033[0m"
        # Assert that the error message is correct after formatting
        self.assertEqual(formatted_output, expected_output)

    @patch('ffmpeg.run')
    @patch('builtins.print')
    @patch('src.ColabKit.media.remove_file')
    def test_ffmpeg_proc_success(self, mock_remove_file, mock_print, mock_run):
        # Test case for a successful FFmpeg process
        mock_run.return_value = None
        result = media.ffmpeg_proc('output_stream', 'output_file', 'message')
        # Assert that the function returned True after executing the FFmpeg process
        self.assertTrue(result)
        # Assert that the print function was called with the expected message
        mock_print.assert_called_with('File message and saved as output_file')
        # Assert that the remove_file function was not called
        mock_remove_file.assert_not_called()

    @patch('ffmpeg.run', side_effect=ffmpeg.Error("", "", stderr=b'Error occurred'))
    @patch('builtins.print')
    @patch('src.ColabKit.media.remove_file')
    def test_ffmpeg_proc_failure(self, mock_remove_file, mock_print, mock_run):
        # Test case for a failed FFmpeg process
        result = media.ffmpeg_proc('output_stream', 'output_file', 'message')
        # Assert that the function returned False after executing the FFmpeg process
        self.assertFalse(result)
        # Assert that the print function was called with the expected message
        mock_print.assert_called_with(media.ffmpeg_err(b'Error occurred'))
        # Assert that the remove_file function was called
        mock_remove_file.assert_called_with('output_file')

    @patch('src.ColabKit.media.ffmpeg_proc', return_value=True)
    @patch('builtins.print')
    def test_ffmpeg_conv_success(self, mock_print, mock_ffmpeg_proc):
        # Test case for a successful conversion
        result = media.ffmpeg_conv('input_file.mp4', 'output_file.mp4')
        # Assert that the function returned True after executing the FFmpeg process
        mock_print.assert_called_with(
            "Converting input_file.mp4 to output_file.mp4...")
        # Assert that the remove_file function was called
        self.assertTrue(result)

    @patch('src.ColabKit.media.ffmpeg_proc', return_value=False)
    @patch('builtins.print')
    def test_ffmpeg_conv_failure(self, mock_print, mock_ffmpeg_proc):
        # Test case for a failed conversion
        result = media.ffmpeg_conv('input_file.mp4', 'output_file.mp4')
        # Assert that the function returned False after executing the FFmpeg process
        mock_print.assert_called_with(
            "Converting input_file.mp4 to output_file.mp4...")
        # Assert that the remove_file function was called
        self.assertFalse(result)

    @patch('src.ColabKit.media.ffmpeg_proc', return_value=True)
    @patch('builtins.print')
    def test_ffmpeg_trim_success(self, mock_print, mock_ffmpeg_proc):
        # Test case for a successful trim
        result = media.ffmpeg_trim('input_file.mp4', 10, 5, 'output_file.mp4')
        # Assert that the function returned True after executing the FFmpeg process
        mock_print.assert_called_with(
            "Trimming input_file.mp4 to 5 seconds...")
        # Assert that the remove_file function was called
        self.assertTrue(result)

    @patch('src.ColabKit.media.ffmpeg_proc', return_value=False)
    @patch('builtins.print')
    def test_ffmpeg_trim_failure(self, mock_print, mock_ffmpeg_proc):
        # Test case for a failed trim
        result = media.ffmpeg_trim('input_file.mp4', 10, 5, 'output_file.mp4')
        # Assert that the function returned False after executing the FFmpeg process
        mock_print.assert_called_with(
            "Trimming input_file.mp4 to 5 seconds...")
        # Assert that the remove_file function was called
        self.assertFalse(result)

    @patch('src.ColabKit.media.get_video_resolution', return_value=(1920, 1080))
    @patch('src.ColabKit.media.ffmpeg_proc', return_value=True)
    @patch('builtins.print')
    def test_resize_video_success(self, mock_print, mock_ffmpeg_proc, mock_get_video_resolution):
        # Test case for a successful resize
        result = media.resize_video('input_video.mp4', 720)
        # Assert that the function returned True after executing the FFmpeg process
        mock_print.assert_called_with("Resizing video to 720p...")
        # Assert that the remove_file function was called
        self.assertEqual(result, 'input_video_720p.mp4')

    @patch('src.ColabKit.media.get_video_resolution', return_value=(1280, 720))
    @patch('src.ColabKit.media.ffmpeg_proc', return_value=True)
    @patch('builtins.print')
    def test_resize_video_small_resolution(self, mock_print, mock_ffmpeg_proc, mock_get_video_resolution):
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
    @patch('src.ColabKit.media.ffmpeg_proc', return_value=False)
    @patch('builtins.print')
    def test_resize_video_failure(self, mock_print, mock_ffmpeg_proc, mock_get_video_resolution):
        # Test case for a failed resize
        result = media.resize_video('input_video.mp4', 720)
        # Assert that the function returned False after executing the FFmpeg process
        mock_print.assert_called_with("Resizing video to 720p...")
        # Assert that the remove_file function was called
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
