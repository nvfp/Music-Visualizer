import datetime
import re
import sys
from typing import NoReturn


def printer(__msg: str, /) -> None:
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {__msg}')

def error(__msg: str, /) -> NoReturn:
    printer(f'Error: {__msg}')
    sys.exit(1)

def convert(hex):
    return hex.replace('#', '0x')

def hex_to_rgb(hex: str, /) -> tuple[int, int, int]:
    return tuple(
        int(hex[i:i + 2], 16)
        for i in (1, 3, 5)
    )

def validate_hex(hex: str, /):
    if not re.match(r'^#[a-fA-F0-9]{6}$', hex):
        error(f'Invalid hexcode: {hex}')