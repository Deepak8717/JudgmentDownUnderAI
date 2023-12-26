from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sys

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'Restarting due to changes in {event.src_path}')
        subprocess.run(["python", sys.argv[1]])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run.py <script.py>")
        sys.exit(1)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()

    try:
        print(f"Watching for changes in {sys.argv[1]}...")
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
