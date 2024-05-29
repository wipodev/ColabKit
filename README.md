<p align="center">
  <img src="https://github.com/wipodev/ColabKit/blob/main/ColabKit.png" alt="ColabKit logo" width="250" height="250">
</p>

# ColabKit ![PyPI - Version](https://img.shields.io/pypi/v/ColabKit) ![PyPI - Downloads](https://img.shields.io/pypi/dm/ColabKit) ![PyPI - License](https://img.shields.io/pypi/l/ColabKit)

ColabKit is a Python library designed to enhance the experience of working in Google Colab environments. With ColabKit, you can simplify common tasks, manipulate media, record audio, and create interactive widgets more efficiently.

## Installation

You can easily install ColabKit using `pip`. Open a terminal and run:

```bash
pip install ColabKit
```

## Test in google colab

You can see the tests carried out on the library in Google Colab through this link

<a href="https://colab.research.google.com/github/wipodev/ColabKit/blob/main/Tests_ColabKit.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

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
