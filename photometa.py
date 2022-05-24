#!/usr/bin/env python3

import os
import argparse
import sys
import subprocess
import json

parser = argparse.ArgumentParser()
parser.add_argument("--year", nargs='+', default='',
                    help='file year')
parser.add_argument("--month", nargs='+', default='',
                    help='file month')
parser.add_argument("--file", nargs='+', default='',
                    help='file name')
parser.add_argument("--title", nargs='+', default='',
                    help='file title (default Untitled)')
parser.add_argument("--location", nargs='+', default='',
                    help='file location')
parser.add_argument("--camera", nargs='+', default='',
                    help='file camera')
parser.add_argument("--desc", nargs='+', default='',
                    help='file description (optional)')
args = parser.parse_args()

def run_command(command, path, ensure_pass=True, get_result=False):
    # Use LC_ALL=C to make sure command output use English.
    # Then we can use English keyword to check command output.
    english_env = os.environ.copy()
    english_env['LC_ALL'] = 'C'

    if get_result:
        process = subprocess.Popen(command, env = english_env, stdin = subprocess.PIPE,
                                   universal_newlines=True, text=True, cwd=path,
                                   stdout = subprocess.PIPE)
    else:
        process = subprocess.Popen(command, env = english_env, stdin = subprocess.PIPE,
                                   universal_newlines=True, text=True, cwd=path)
    process.wait()
    if process.returncode != 0 and ensure_pass:
        sys.exit(process.returncode)
    if get_result:
        return process.stdout.readlines()
    else:
        return None

def main():
    meta_json = {
        'file': '',
        'title': 'Untitled',
        'location': '',
        'year': '',
        'month': '',
        'camera': 'Fujifilm XPro3',
        'aperture': '',
        'ss': '',
        'iso': '',
        'lens': '',
        'desc': ''
    }

    if len(args.year) == 0 or len(args.month) == 0 or len(args.file) == 0:
        raise Exception('Must specify year, month, and file!')
    else:
        meta_json['year'] = args.year[0]
        meta_json['month'] = args.month[0]
        meta_json['file'] = args.file[0]

    if len(args.title) > 0:
        meta_json['title'] = ' '.join(args.title)
    if len(args.desc) > 0:
        meta_json['desc'] = ' '.join(args.desc)
    if len(args.location) > 0:
        meta_json['location'] = ' '.join(args.location)
    if len(args.camera) > 0:
        meta_json['camera'] = ' '.join(args.camera)

    top_path_outputs = run_command(['git', 'rev-parse', '--show-toplevel'], path=os.getcwd(), get_result=True)
    if top_path_outputs is None:
        raise Exception('No git top-level output')
    top_path = top_path_outputs[0].strip()
    path = os.path.join(top_path, 'gallery', 'full', meta_json['year'], meta_json['month'])
    file_path = os.path.join(path, meta_json['file'])
    meta_outputs = run_command(['exiftool', file_path], path=path, get_result=True)

    if meta_outputs is None:
        raise Exception('Something went wrong with exiftool!')

    def get_meta_output(line):
        return line.split(':')[1].strip()

    for meta in meta_outputs:
        if 'Exposure Time' in meta:
            meta_json['ss'] = get_meta_output(meta)
        elif 'F Number' in meta:
            meta_json['aperture'] = 'f/' + get_meta_output(meta)
        elif 'ISO' in meta:
            meta_json['iso'] = get_meta_output(meta)
        elif 'Lens Info' in meta:
            lens_info = get_meta_output(meta)
            if '56mm' in lens_info and '1.2' in lens_info:
                meta_json['lens'] = 'Fujinon XF56mmf1.2'
            elif '23mm' in lens_info and '2' in lens_info:
                meta_json['lens'] = 'Fujinon XF23mmf2'
            elif '35mm' in lens_info and '1.4' in lens_info:
                meta_json['lens'] = 'Fujinon XF35mmf1.4'
    print(json.dumps(meta_json, indent = 4)+',')


if __name__ == '__main__':
    main()
