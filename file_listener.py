import os
import textract
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

folder_to_watch = "./depots"

# Get the absolute path to the folder
folder_path = os.path.abspath(folder_to_watch)


def clean_text(text):
    pattern = r'[^\x00-\x7F]+'  # Matches non-ASCII characters
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def extract_text(file_path):
    try:
        text = textract.process(file_path).decode("utf-8")
        return clean_text(text)
    except Exception as e:
        print(f"Error: {e}")
        return None


class FileHandler(FileSystemEventHandler):
    def __init__(self):
        self.newly_created_file = None
        self.should_stop = False

    def on_created(self, event):
        if not event.is_directory:
            self.newly_created_file = event.src_path

    def get_newly_created_file(self):
        return self.newly_created_file

    def should_stop_processing(self):
        return self.should_stop

    def set_stop_condition(self, value):
        self.should_stop = value
