<p align="center">
  <img src="ColabKit.jpg" alt="ColabKit logo" width="250" height="250">
</p>

---

# ColabKit

ColabKit is a Python library designed to enhance the experience of working in Google Colab environments. With ColabKit, you can simplify common tasks, manipulate media, record audio, and create interactive widgets more efficiently.

## Installation

You can easily install ColabKit using `pip`. Open a terminal and run:

```bash
pip install -i https://test.pypi.org/simple/ ColabKit==0.0.1a0
```

**Please note**: ColabKit is currently in an alpha testing phase. Make sure to check for updates and newer versions as the library evolves.

## Key Features

- **Media Manipulation**: Visualize and edit video and audio files directly in your notebook.
- **Audio Recording**: Record real-time audio through your browser with a simple function.
- **Interactive Widgets**: Create interactive buttons in the notebook to execute custom code.
- **System Utilities**: Simplify common tasks, such as file deletion and file existence checks.

## Usage Examples

### Video Display

```python
from ColabKit.media import showMedia

# Display a video file
showMedia('video.mp4', 'video')
```

### Audio Recording

```python
from ColabKit.record import record

# Record audio and save the result to a WAV file
record('recording.wav')
```

### Creating Interactive Buttons

```python
from ColabKit.widget import button

# Create an interactive button
def my_function():
    print("You clicked the button!")

button("Click Me", "Click to execute my_function", "success", my_function)
```

## Documentation

For more information and detailed documentation, visit [the ColabKit repository on GitHub](https://github.com/wipodev/ColabKit).

## Contributions

We appreciate contributions! If you wish to contribute or report issues, visit [our GitHub repository](https://github.com/wipodev/ColabKit).

## License

This project is under the MIT License. See the [LICENSE](https://github.com/wipodev/ColabKit/blob/main/LICENSE) file for more details.

---
