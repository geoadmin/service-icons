import argparse as ap
import logging
import os
import sys
from textwrap import dedent

import cairosvg

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def create_parser():
    parser = ap.ArgumentParser(
        description=dedent(
            """\
        Purpose:
            This script is used to transform svg images into png

        Example usage:

        Transforming svg images into png using a source and a destination folder:
          svg2png.py
          --width 48
          --height 48
          --input /tmp/babs2
          --output ../app/static/images/babs2
            """
        ),
        formatter_class=ap.RawDescriptionHelpFormatter
    )

    option_group = parser.add_argument_group('Program options')
    option_group.add_argument(
        '-I',
        '--input',
        dest='input',
        action='store',
        type=the_dir,
        required=True,
        help='The dir where the svg images are located'
    )

    option_group.add_argument(
        '-O',
        '--output',
        dest='output',
        action='store',
        type=the_dir,
        required=True,
        help='The dir where the png images will be stored'
    )

    option_group.add_argument(
        '-W',
        '--width',
        dest='width',
        action='store',
        default=None,
        type=pixel_size,
        help='The width in pixel of the png image'
    )

    option_group.add_argument(
        '-H',
        '--height',
        dest='height',
        action='store',
        default=None,
        type=pixel_size,
        help='The width in pixel of the png image'
    )

    option_group.add_argument(
        '-R',
        '--dpi',
        dest='dpi',
        action='store',
        default=92,
        type=dpi,
        help='The resolution of the png image'
    )

    option_group.add_argument(
        '-D',
        '--dryrun',
        dest='dryrun',
        action='store_false',
        default=True,
        help='The width in pixel of the png image'
    )

    return parser


def dpi(d):
    d = float(d)  # this may lead to an error, but that is ok
    if d > 20:
        return d
    logger.error("The resolution has to be bigger than 20 dpi")
    sys.exit(1)


def pixel_size(size):
    size = float(size)  # this may lead to an error, but that is ok
    if size > 0.0:
        return size
    logger.error("size (width and heigh) has to be > 0")
    sys.exit(1)


def the_dir(d):
    if len(d) > 0:
        return d
    logger.error("the path has to be specified")
    sys.exit(1)


def validate_args(argv):
    parser = create_parser()
    the_opts = parser.parse_args(argv[1:])
    return the_opts


def svg2png():
    # create output folder if not exists
    if not os.path.exists(opts.output):
        os.makedirs(opts.output)

    for file in os.listdir(opts.input):
        if file.endswith(".svg"):
            svg_image = os.path.join(opts.input, file)
            png_image = os.path.join(opts.output, file[:-3] + 'png')
            if opts.dryrun:
                logger.debug("Treating image: %s > %s", svg_image, png_image)
                cairosvg.svg2png(
                    dpi=opts.dpi,
                    file_obj=open(svg_image, "rb"),  # pylint: disable=consider-using-with
                    write_to=png_image,
                    output_height=opts.height,
                    output_width=opts.width
                )
            else:
                logger.debug("dryrun image: %s > %s", svg_image, png_image)


def main():
    global opts  # pylint: disable=global-variable-undefined
    opts = validate_args(sys.argv)
    svg2png()


if __name__ == '__main__':
    main()
