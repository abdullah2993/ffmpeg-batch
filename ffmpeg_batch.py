import ffmpeg
import os
from os import path

from argparse import ArgumentParser
from shutil import copyfile

DEBUG = False


def main():
    parser = ArgumentParser(description='Batch covnert directories')
    parser.add_argument('source', help='Source directory')
    parser.add_argument('dest', help='Destination directory')
    parser.add_argument('-e', '--ext', nargs='+', help='Extension')
    parser.add_argument('-c', '--copy', action='store_true',
                        help='Copy other files')
    parser.add_argument('-l', '--log',
                        default='.__convlog.log', help='Record file')
    parser.add_argument('-v', '--verbose',
                        action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        global DEBUG
        DEBUG = True

    log('Converting {} to {}', args.source, args.dest)
    if not path.exists(args.dest):
        log('Creating {}', args.dest)
        os.makedirs(args.dest)
    else:
        log('Conversion directory already exist {}', args.dest)

    log('Looking for record file', args.log)
    logfp = path.join(args.dest, args.log)
    if not path.exists(logfp):
        log('Record file does not exist')

    logf = open(logfp, 'a+')
    lines = [x.strip() for x in logf.readlines()]

    log("{} records found", len(lines))

    for root, dirs, files in os.walk(args.source):
        rel = path.relpath(root, args.source)
        for d in dirs:
            dd = path.join(args.dest, rel , d)
            if not path.exists(dd):
                log('Creating {}', dd)
                os.makedirs(dd)

        for f in files:
            ext = path.splitext(f)
            sf = path.join(root, f)
            if sf in lines:
                log("Skipping {}", sf)
                continue
            df = path.join(args.dest, rel, f)
            if args.ext is None or len(ext) > 1 and ext[1] in args.ext:
                try:
                    log('Converting {} to {}', sf, df)
                    cmd = (ffmpeg.input(sf)
                           .output(df, s='hd480')
                           .global_args('-hide_banner')
                           .global_args('-loglevel', 'quiet')
                           .global_args('-stats')
                           .overwrite_output())

                    log('Executing ffmpeg: {}', ' '.join(cmd.compile()))
                    cmd.run()
                    logf.write(sf + '\r\n')
                except ffmpeg.Error as e:
                    log('Error occured on file {}: {}', sf, e)
            elif args.copy:
                log('Copying file {} to {}', sf, df)
                copyfile(sf, df)
                logf.write(sf + '\r\n')
            else:
                log("File not processed {}", sf)

    logf.close()


def log(msg, *args):
    if DEBUG:
        print(msg.format(*args))


if __name__ == '__main__':
    main()
