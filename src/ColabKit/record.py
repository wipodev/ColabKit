from .template import AUDIO_RECORD, SAVED_AUDIO_RECORDING
from scipy.io.wavfile import read as wav_read, write as wav_write
from IPython.display import HTML, display
if 'google.colab' in globals():
    from google.colab.output import eval_js
from .utils import wait_for_file
from base64 import b64decode
import ffmpeg
import io


def get_audio() -> tuple:
    display(HTML(AUDIO_RECORD))
    data = eval_js("data")
    binary = b64decode(data.split(',')[1])
    process = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', format='wav')
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, quiet=True, overwrite_output=True)
    )
    output, err = process.communicate(input=binary)
    riff_chunk_size = len(output) - 8
    q = riff_chunk_size
    b = []
    for i in range(4):
        q, r = divmod(q, 256)
        b.append(r)
    riff = output[:4] + bytes(b) + output[8:]
    sr, audio = wav_read(io.BytesIO(riff))
    return audio, sr


def record(file_audio="record.wav") -> None:
    audio, sr = get_audio()
    wav_write(file_audio, sr, audio)
    if wait_for_file(file_audio):
        display(HTML(SAVED_AUDIO_RECORDING))
