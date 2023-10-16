if 'google.colab' in globals():
    from google.colab import files, drive
import time
import os


def remove_file(route) -> None:
    if os.path.isfile(route):
        os.remove(route)


def file_exists(route) -> bool:
    return os.path.exists(route)


def mount_drive() -> None:
    if not os.path.isdir("/content/drive/MyDrive"):
        drive.mount('/content/drive', force_remount=True)


def upload_file(route) -> None:
    remove_file(route)
    uploaded = files.upload()
    for filename in uploaded.keys():
        os.rename(filename, route)


def wait_for_file(file_name: str, time_limit: int = 60) -> bool:
    initial_time = time.time()
    exists = False

    while time.time() - initial_time < time_limit:
        if os.path.exists(file_name):
            previous_size = os.path.getsize(file_name)
            time.sleep(1)
            current_size = os.path.getsize(file_name)
            if current_size == previous_size:
                exists = True
                break
    return exists
