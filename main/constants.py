import os


SOFTWARE_VER = '1.0.0'
SOFTWARE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOFTWARE_NAME = os.path.basename(SOFTWARE_DIR)

## default
INPUT_DIR = os.path.join(SOFTWARE_DIR, 'input')
OUTPUT_DIR = os.path.join(SOFTWARE_DIR, 'output')

TYPES = (
    '.mp3',
    '.m4a',
    '.wav',
    '.aac',
    '.ogg',
    '.flac',
    '.wma',
    '.alac',
    '.aiff'
)