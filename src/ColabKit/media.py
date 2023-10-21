from .template import VIDEO_SHOW, AUDIO_SHOW
from .utils import file_exists, remove_file
from IPython.display import display, HTML
from base64 import b64encode
import ffmpeg


def showMedia(file_path, media) -> None:
    if file_exists(file_path):
        content_type = 'video/mp4' if media == "video" else 'audio/wav'
        media_type = VIDEO_SHOW if media == "video" else AUDIO_SHOW
        data = open(file_path, 'rb').read()
        data_url = f"data:{content_type};base64," + b64encode(data).decode()
        display(HTML(media_type % data_url))
    else:
        print(
            f"\033[43m\033[101mThe {media} file {file_path} is not found in the directory.\033[0m")


def get_duration(file) -> float:
    info = ffmpeg.probe(file)
    return float(info['format']['duration'])


def get_video_resolution(file) -> tuple:
    info = ffmpeg.probe(file)['streams'][0]
    if "video" == info['codec_type']:
        return (info['width'], info['height'])
    print(
        f"\033[43m\033[101mFile {file} is not a valid parameter, you must provide an audio file\033[0m")


def get_formatted_error(stderr) -> str:
    lines = stderr.decode('utf-8').splitlines()
    error_lines = [line for line in lines if line.startswith("Error")]
    for error_line in error_lines:
        return f"\033[43m\033[101m{error_line}\033[0m"


def run_process(output_stream, output_file, msg) -> bool:
    try:
        ffmpeg.run(output_stream, capture_stderr=True, overwrite_output=True)
        print(f'File {msg} and saved as {output_file}')
        return True
    except ffmpeg.Error as e:
        print(get_formatted_error(e.stderr))
        remove_file(output_file)
        return False


def convert(input_file: str, output_file: str) -> bool:
    print(f"Converting {input_file} to {output_file}...")
    input_stream = ffmpeg.input(input_file)
    output_stream = ffmpeg.output(input_stream, output_file)
    return run_process(output_stream, output_file, "converted")


def shorten(input_file, start, interval, output_file) -> str:
    print(f"Trimming {input_file} to {interval} seconds...")
    input_stream = ffmpeg.input(input_file, ss=start)
    output_stream = ffmpeg.output(input_stream, output_file, t=interval)
    return run_process(output_stream, output_file, "trimmed")


def resize_video(video_path: str, new_resolution: int):
    new_path = f"{video_path.split('.')[0]}_{new_resolution}p.mp4"
    video_resolution = get_video_resolution(video_path)
    print(f"Video resolution: {video_resolution}")
    if video_resolution[0] >= 1920 or video_resolution[1] >= 1080:
        print(f"Resizing video to {new_resolution}p...")
        new_width = 2 * \
            int((video_resolution[0] /
                video_resolution[1] * new_resolution / 2))
        input_stream = ffmpeg.input(video_path)
        output_stream = ffmpeg.output(
            input_stream, new_path, vf=f'scale={new_width}:{new_resolution}', vcodec='libx264')
        return new_path if run_process(output_stream, new_path, "resized") else False
    else:
        print("No need to change the size")
        return video_path
