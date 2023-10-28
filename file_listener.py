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


def clean_text(text):
    pattern = r'[^\x00-\x7F]+'  # Matches non-ASCII characters
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def extract_text(file_path):
    try:
        #file_path = FileHandler().on_created
        #print(file_path)
        #print(type(file_path))
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
            #print(f"Newly created file: {event.src_path}")
            self.newly_created_file = event.src_path

    def get_newly_created_file(self):
        return self.newly_created_file

    def should_stop_processing(self):
        return self.should_stop

    def set_stop_condition(self, value):
        self.should_stop = value

"""if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path)
    observer.start()
    try:
        while True:
            if event_handler.newly_created_file:
                print("Newly created file:", event_handler.newly_created_file)

    except KeyboardInterrupt:
        observer.stop()
        observer.join() """
