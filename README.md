# ffmpeg-batch
Convert a directory tree using ffmpeg

## Usage
```
usage: ffmpeg_batch.py [-h] [-e EXT [EXT ...]] [-c] [-l LOG] [-v] source dest

Batch covnert directories

positional arguments:
  source                Source directory
  dest                  Destination directory

optional arguments:
  -h, --help            show this help message and exit
  -e EXT [EXT ...], --ext EXT [EXT ...]
                        Extension
  -c, --copy            Copy other files
  -l LOG, --log LOG     Record file
  -v, --verbose         Verbose output

```