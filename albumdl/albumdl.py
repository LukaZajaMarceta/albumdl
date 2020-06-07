#!/usr/bin/env python3

from . import videolink, cfg
import argparse
import sys


def parser():
    parser = argparse.ArgumentParser(description='tool to download albums from youtube with sliced songs')

    parser.add_argument('youtube_url', metavar='URL', nargs=1,
                        help='url of youtube video')
    parser.add_argument('-o', '--output',
                        help='folder to save album for this video')
    parser.add_argument('-O', '--default_output',
                        help='change the default output folder')
    parser.add_argument('-c', '--comments', action='store_true',
                        help='lists the comments that could hold song timestamps')
    parser.add_argument('-C', '--comment', type=int, default=0,
                        help='''selects specific comment to yield song timestamps
                        use -c to see possible options''')
    parser.add_argument('-a', '--album_name', default=None,
                        help='specify album name, default is video name')
    parser.add_argument('-A', '--album_folder', action='store_false', default=True,
                        help='if used separate album folder will NOT be created')

    return parser.parse_args()


def main():
    args = parser()
    if args.default_output:
        cfg.set_default(args.default_output)
    output = args.output if args.output else cfg.get_default()
    link = args.youtube_url[0]
    VL = videolink.VideoLink(link)
    cfg.save()
    if args.comments:
        VL.print_comments()
        sys.exit()
    if args.comment:
        VL.set_timestamps_comment(args.comment)
    VL(output, album_name=args.album_name, make_folder=args.album_folder)


if __name__ == '__main__':
    main()











