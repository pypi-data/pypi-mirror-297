"""pysnarf."""

import argparse
import os
import threading
import time
from pathlib import Path
from typing import Union

import clipboard_monitor
import pyperclip
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

parser = argparse.ArgumentParser()

parser.add_argument(
    "snarf",
    type=lambda f: Path(f).absolute(),
    help="Path to .snarf file or dir.",
)


def main():
    """Main."""

    thread_lock = threading.Lock()

    args = parser.parse_args()

    if args.snarf.is_dir():
        args.snarf = (args.snarf / ".snarf").absolute()

    if not args.snarf.exists():
        args.snarf.touch()

    print(f"Opening {args.snarf}")

    class SnarfHandler(FileSystemEventHandler):
        """FileHandler."""

        def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]) -> None:
            with thread_lock:
                if event.src_path == str(args.snarf):
                    with args.snarf.open("rb") as f:
                        if os.name == "nt":
                            txt: str = f.read().replace(b"\n", b"\r\n").decode()
                        else:
                            txt = f.read().decode()
                        if txt != pyperclip.paste():
                            pyperclip.copy(txt)

    def snarf_paste(text: str):
        with thread_lock:
            with args.snarf.open("wb") as f:
                f.write(text.encode().replace(b"\r\n", b"\n"))

    handler = SnarfHandler()

    observer = Observer()
    observer.schedule(event_handler=handler, path=args.snarf.parent)
    observer.start()

    clipboard_monitor.on_text(snarf_paste)

    while clipboard_monitor._clipboard_thread.is_alive() and observer.is_alive():
        time.sleep(1)


if __name__ == "__main__":
    main()
