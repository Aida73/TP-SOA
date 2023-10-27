import os
import textract
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

# Define the directory to monitor (assuming it's in the same directory as your script)
folder_to_watch = "./depots"  # Replace this with the directory you want to monitor

# Get the absolute path to the folder
folder_path = os.path.abspath(folder_to_watch)


class FileHandler(FileSystemEventHandler):
    def __init__(self):
        self.newly_created_file = None

    def on_created(self, event):
        if not event.is_directory:
            print(f"Newly created file: {event.src_path}")
            self.newly_created_file = event.src_path
            return event.src_path


def clean_text(text):
    pattern = r'[^\x00-\x7F]+'  # Matches non-ASCII characters
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def extract_text():
    try:
        text = textract.process(FileHandler().on_created).decode("utf-8")
        return clean_text(text)
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=False)
    observer.start()

    try:
        while True:
            if event_handler.newly_created_file:
                print("Newly created file:", event_handler.newly_created_file)
                # Do something with the file path, and then reset it
                event_handler.newly_created_file = None
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
