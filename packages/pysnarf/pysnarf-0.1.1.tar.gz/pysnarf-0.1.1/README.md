# pysnarf

Multi-platform .[snarf](https://wiki.xxiivv.com/site/snarf.html) file integration with the clipboard, written in python.

Made for use with [Uxn](https://100r.co/site/uxn.html).

## Installation

```sh
pip install pysnarf
```

## Usage

Simply run `pysnarf path-to-.snarf-file-or-dir`.

If a directory is passed, the script will find the `.snarf` file or generate it if not present.

On Windows, copying/pasting does a `LF <> CRLF` replacement (as Uxn likes).
