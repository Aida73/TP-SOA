import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the directory to monitor (assuming it's in the same directory as your script)


folder_to_watch = "./depots"  # Ajouter le dossier

# Get the absolute path to the folder
folder_path = os.path.abspath(folder_to_watch)


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            return event.src_path


if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
