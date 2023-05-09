import argparse
import os
import subprocess as sp

from main.constants import SOFTWARE_VER, SOFTWARE_NAME, INPUT_DIR, OUTPUT_DIR, TYPES
from main.utils import printer, error, convert, validate_hex


parser = argparse.ArgumentParser(prog=SOFTWARE_NAME, description='Watch the music with visualization using FFmpeg')
parser.add_argument('--version', action='version', version=f'%(prog)s {SOFTWARE_VER}')

parser.add_argument(
    '-i', '--input',
    default=INPUT_DIR,
    help=f'Absolute path to input file (single input) or directory (multiple inputs). Default: {repr(INPUT_DIR)}'
)
parser.add_argument(
    '-o', '--output',
    # default=OUTPUT_DIR,  # this line purposely commented to make the default set to `None`
    help=(
        'If -i is a directory path, the output folder will be set to the input folder. '
        f'Otherwise, if -i is a file path or not specified, the default {repr(OUTPUT_DIR)} will be used.'
    )
)
parser.add_argument(
    '-ff', '--ffmpeg',
    default='ffmpeg',
    help='FFmpeg binary file path or command (default: \'ffmpeg\')'
)

parser.add_argument(
    '-g', '--use_gpu',
    help=f'Use -g a for AMD GPU, -g n for NVIDIA GPU. Default is using CPU.'
)
parser.add_argument(
    '-q', '--quality',
    type=int, default=18,
    help=(
        'A decent -q range is typically 10-33 for GPU and 10-30 for CPU. '
        'Use -q 0 for full quality; default is 18. '
        'Note the trade-off between quality and compression rate.'
    )
)
parser.add_argument(
    '-r', '--frame_rate',
    type=int, default=24,
    help='The number of frames per second (FPS) for the output, default is 24.'
)

parser.add_argument(
    '-tf', '--title_font',
    default='c\:/Windows/Fonts/Arial.ttf',
    help=(
        'Font that used for words like "CQT" and "Diff". '
        'Specify the absolute path to the font file. '
        'Linux/Unix (~/.fonts/arial.ttf), Windows (C:\Windows\Fonts\\arial.ttf), MacOS (/Library/Fonts/Arial.ttf). '
        'Default font: "c\:/Windows/Fonts/Arial.ttf"'
    )
)
parser.add_argument(
    '-tc', '--title_color',
    default='#cacbca',
    help='In hexadecimal format. Default: #cacbca'
)
parser.add_argument(
    '-pc', '--pad_color',
    default='#e6cbe6',
    help='The border color. Default: #e6cbe6'
)

parser.add_argument(
    '-ccl', '--cqt_color_left',
    default='#2673d9',
    help='CQT color, for the left channel. Default: #2673d9'
)
parser.add_argument(
    '-ccr', '--cqt_color_right',
    default='#03753d',
    help='CQT color, for the right channel. Default: #03753d'
)
parser.add_argument(
    '-cg', '--cqt_gamma',
    type=int, default=1,
    help=(
        'Lower gamma makes the spectrum more contrast, '
        'higher gamma makes the spectrum having more range. '
        'Interval: [1, 7]. Default: 1'
    )
)
parser.add_argument(
    '-cbt', '--cqt_bar_transparency',
    type=float, default=0.9,
    help='Interval: [0, 1]. Default: 0.9'
)
parser.add_argument(
    '-cbv', '--cqt_bar_volume',
    type=int, default=10,
    help='Interval: [0, 100]. Default: 10'
)
parser.add_argument(
    '-ctc', '--cqt_timeclamp',
    type=float, default=0.15,
    help=(
        'According to the FFmpeg documentation, '
        'At low frequency, there is trade-off between accuracy in time domain and frequency domain. '
        'If timeclamp is lower, event in time domain is represented more accurately (such as fast bass drum), '
        'otherwise event in frequency domain is represented more accurately (such as bass guitar). '
        'Interval: [0.002, 1]. Default: 0.15'
    )
)
parser.add_argument(
    '-cnf', '--cqt_notes_font',
    default='c\:/Windows/Fonts/courbd.ttf',
    help='Absolute path to the font file; monospace font is recommended. Default: Courier New Bold'
)

parser.add_argument(
    '-dca', '--diff_color_add',
    default='#bddefa',
    help='Color to be added to represent channel vectors each frame. Default: #bddefa'
)
parser.add_argument(
    '-dcf', '--diff_color_fade',
    default='#fdbbdc',
    help='Color to be faded to represent channel vectors each frame. Default: #fdbbdc'
)
parser.add_argument(
    '-dr', '--diff_rotate',
    type=int, default=9,
    help='Rotation, in degrees. Interval: [0, 359]. Default: 9 deg.'
)

parser.add_argument(
    '-sc', '--spec_color',
    default='intensity',
    help=(
        'The spectrum color types. '
        'Options: channel, intensity, rainbow, moreland, nebulae, '
        'fire, fiery, fruit, cool, magma, green, viridis, plasma, '
        'cividis, terrain. Default: intensity'
    )
)
parser.add_argument(
    '-ss', '--spec_scale',
    default='5thrt',
    help='Options: lin, sqrt, cbrt, 4thrt, 5thrt, log. Default: 5thrt'
)
parser.add_argument(
    '-ssa', '--spec_saturation',
    type=float, default=1,
    help='Interval: [-10.0, 10.0]. Default: 1'
)
parser.add_argument(
    '-swf', '--spec_win_func',
    default='dolph',
    help=(
        'Options: rect, bartlett, hann, hanning, hamming, blackman, '
        'welch, flattop, bharris, bnuttall, bhann, sine, nuttall, '
        'lanczos, gauss, tukey, dolph, cauchy, parzen, poisson, '
        'bohman. Default: dolph'
    )
)
parser.add_argument(
    '-sdr', '--spec_drange',
    type=int, default=24,
    help=(
        'Dynamic range (in dBFS) used to calculate intensity color values. '
        'Interval: [10, 200]. Default: 24'
    )
)

parser.add_argument(
    '-wcl', '--waves_color_left',
    default='#ff4949',
    help='For the left channel. Default: #ff4949'
)
parser.add_argument(
    '-wcr', '--waves_color_right',
    default='#4dbffc',
    help='For the right channel. Default: #4dbffc'
)
parser.add_argument(
    '-vc', '--vol_color',
    default='#032341',
    help='Volume bars color. Default: #032341'
)

args = parser.parse_args()


printer('INFO: Validating the arguments..')

FFMPEG = args.ffmpeg
if FFMPEG != 'ffmpeg':
    if not (os.path.isfile(FFMPEG) and os.path.splitext(FFMPEG.lower())[1] == '.exe'):
        error('FFMPEG path is invalid or does not point to an ffmpeg executable.')
try:
    sp.run([FFMPEG, '-version'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    printer(f'INFO: ffmpeg valid and usable.')
except FileNotFoundError:
    error(f'ffmpeg not found or not a recognized command ({FFMPEG})')

if args.use_gpu not in {'a', 'n', None}:
    error('Invalid `use_gpu` value')
if not (0 <= args.quality <= 51):
    error('Invalid `quality` value')
if not (1 <= args.frame_rate <= 120):
    error('Invalid `frame_rate` value')

validate_hex(args.title_color)
validate_hex(args.pad_color)

validate_hex(args.cqt_color_left)
validate_hex(args.cqt_color_right)
if not (1 <= args.cqt_gamma <= 7):
    error('Invalid `cqt_gamma` value')
if not (0 <= args.cqt_bar_transparency <= 1):
    error('Invalid `cqt_bar_transparency` value')
if not (0 <= args.cqt_bar_volume <= 100):
    error('Invalid `cqt_bar_volume` value')
if not (0.002 <= args.cqt_timeclamp <= 1):
    error('Invalid `cqt_timeclamp` value')

validate_hex(args.diff_color_add)
validate_hex(args.diff_color_fade)
if not (0 <= args.diff_rotate <= 359):
    error('Invalid `diff_rotate` value')

if args.spec_color not in [
    'channel', 'intensity', 'rainbow', 'moreland', 'nebulae', 'fire', 'fiery',
    'fruit', 'cool', 'magma', 'green', 'viridis', 'plasma', 'cividis', 'terrain'
]:
    error('Invalid `spec_color` value')
if args.spec_scale not in ['lin', 'sqrt', 'cbrt', '4thrt', '5thrt', 'log']:
    error('Invalid `spec_scale` value')
if not (-10 <= args.spec_saturation <= 10):
    error('Invalid `spec_saturation` value')
if args.spec_win_func not in [
    'rect', 'bartlett', 'hann', 'hanning', 'hamming', 'blackman', 'welch', 'flattop',
    'bharris', 'bnuttall', 'bhann', 'sine', 'nuttall', 'lanczos', 'gauss', 'tukey',
    'dolph', 'cauchy', 'parzen', 'poisson', 'bohman'
]:
    error('Invalid `spec_win_func` value')
if not (10 <= args.spec_drange <= 200):
    error('Invalid `spec_drange` value')

validate_hex(args.waves_color_left)
validate_hex(args.waves_color_right)
validate_hex(args.vol_color)


class Args:
    ffmpeg_pth = FFMPEG

    if args.input == INPUT_DIR:
        input = os.listdir(INPUT_DIR)
        input.remove('.gitkeep')
        input = [
            os.path.join(INPUT_DIR, f)
            for f in input
        ]
    else:
        if os.path.isfile(args.input):
            input = [args.input]
        elif os.path.isdir(args.input):
            input = [
                os.path.join(args.input, f)
                for f in os.listdir(args.input)
            ]
        else:
            error(f'Invalid input: {args.input}')
    if len(input) < 1:
        error('No input detected.')
    for i in input:
        if not i.lower().endswith(TYPES):
            error(f'Invalid types: {i}')
    printer(f'INFO: Inputs: {len(input)} file(s) found.')

    if args.output is None:
        if args.input == INPUT_DIR:
            output = OUTPUT_DIR
        else:
            if os.path.isfile(args.input):
                output = OUTPUT_DIR
            elif os.path.isdir(args.input):
                output = args.input
    else:
        output = args.output
    printer(f'INFO: output dir set to: {output}')

    Q = str(args.quality)
    if args.use_gpu is None:
        codec = ['-c:v', 'libx264', '-crf', Q]
        printer('INFO: Rendering with CPU')
    elif args.use_gpu == 'a':
        codec = ['-c:v', 'h264_amf', '-rc', 'cqp', '-qp_i', Q, '-qp_p', Q, '-qp_b', Q]
        printer('INFO: Rendering with GPU (h264_amf)')
    elif args.use_gpu == 'n':
        codec = ['-c:v', 'h264_nvenc', '-rc', 'vbr', '-qp', Q]
        printer('INFO: Rendering with GPU (h264_nvenc)')

    r = args.frame_rate

    title_font = args.title_font
    title_color = convert(args.title_color)
    pad_color = convert(args.pad_color)

    ## note, cqt and diff colors should not be converted
    cqt_color_left = args.cqt_color_left
    cqt_color_right = args.cqt_color_right
    cqt_gamma = args.cqt_gamma
    cqt_bar_transparency = args.cqt_bar_transparency
    cqt_bar_volume = args.cqt_bar_volume
    cqt_timeclamp = args.cqt_timeclamp
    cqt_notes_font = args.cqt_notes_font

    ## note, cqt and diff colors should not be converted
    diff_color_add = args.diff_color_add
    diff_color_fade = args.diff_color_fade
    diff_rotate = args.diff_rotate

    spec_color = args.spec_color
    spec_scale = args.spec_scale
    spec_saturation = args.spec_saturation
    spec_win_func = args.spec_win_func
    spec_drange = args.spec_drange

    waves_color_left = convert(args.waves_color_left)
    waves_color_right = convert(args.waves_color_right)

    ## (@ Apr 5, 2023) The author suspects this is a bug from FFmpeg internal.
    ## To get the color right, we need to flip the red and blue channels.
    ## If the bug doesn't exist for your ffmpeg, simply comment out the line below*
    vol_color = '#' + args.vol_color[5:7] + args.vol_color[3:5] + args.vol_color[1:3]
    vol_color = convert(vol_color)
    # vol_color = convert(args.vol_color)  # *and use this instead
