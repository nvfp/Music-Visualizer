import argparse
import datetime
import os
import subprocess as sp
import sys
from typing import NoReturn

from main.constants import SOFTWARE_VER, SOFTWARE_NAME, INPUT_DIR, OUTPUT_DIR


parser = argparse.ArgumentParser(prog=SOFTWARE_NAME, description='')
parser.add_argument('--version', action='version', version=f'%(prog)s {SOFTWARE_VER}')

parser.add_argument('-i', '--input', help='')
parser.add_argument('-o', '--output', help='')

args = parser.parse_args()



def main():
    pass