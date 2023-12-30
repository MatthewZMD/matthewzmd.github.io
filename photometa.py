#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", nargs='+', type=str, default='',
                    help='Photo year')
parser.add_argument("-m", "--month", nargs='+', type=str, default='',
                    help='Photo month')
parser.add_argument("-l", "--location", nargs='+', type=str, default='',
                    help='Photo file location')
parser.add_argument("-f", "--file", nargs='+', type=str, default='',
                    help='Photo filename')
parser.add_argument("-t", "--title", nargs='+', type=str, default='',
                    help='Photo title (default Untitled)')
parser.add_argument("-d", "--desc", nargs='+', type=str, default='',
                    help='Photo description (optional)')
parser.add_argument("-g", "--genre", nargs='+', type=str, default='',
                    help='Photo genre')
parser.add_argument("--camera", nargs='+', type=str, default='',
                    help='Camera used')
parser.add_argument("--lens", nargs='+', type=str, default='',
                    help='Lens used')
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
        'camera': '',
        'aperture': '',
        'ss': '',
        'iso': '',
        'lens': '',
        'desc': '',
        'genre': ''
    }

    if len(args.year) == 0 or len(args.month) == 0 or len(args.file) == 0 or len(args.genre) == 0:
        raise Exception('Must specify year, month, genre, and file!')
    else:
        meta_json['year'] = args.year[0]
        meta_json['month'] = args.month[0]
        meta_json['file'] = args.file[0]
        if args.genre[0] == 's':
            meta_json['genre'] = "streets"
        elif args.genre[0] == 'p':
            meta_json['genre'] = "portraits"
        elif args.genre[0] == 'l':
            meta_json['genre'] = "landscapes"
        elif args.genre[0] == 'i':
            meta_json['genre'] = "interests"
        else:
            meta_json['genre'] = args.genre[0]

    if len(args.title) > 0:
        meta_json['title'] = ' '.join(args.title)
    if len(args.desc) > 0:
        meta_json['desc'] = ' '.join(args.desc)
    if len(args.location) > 0:
        meta_json['location'] = ' '.join(args.location)
    if len(args.camera) > 0:
        meta_json['camera'] = ' '.join(args.camera)
    if len(args.lens) > 0:
        meta_json['lens'] = ' '.join(args.lens)

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

    if "jpeg" in meta_json['file']:
        meta_json['file'] = meta_json['file'].replace("jpeg", "jpg")

    for meta in meta_outputs:
        # print(meta, get_meta_output(meta))
        if 'Camera Model Name' in meta and len(args.camera) == 0:
            camera = get_meta_output(meta)
            if 'X-Pro3' in camera:
                meta_json['camera'] = 'Fujifilm XPro3'
            elif 'RICOH GR III' in camera:
                meta_json['camera'] = 'Ricoh GR3'
                meta_json['lens'] = '27mmf2.8'
            elif 'ILCE-7RM5' in camera:
                meta_json['camera'] = 'Sony A7R5'
            elif '2304FPN6DC' in camera:
                meta_json['camera'] = 'Xiaomi 13 Ultra'
        if 'Exposure Time' in meta:
            meta_json['ss'] = get_meta_output(meta)
        elif 'F Number' in meta:
            meta_json['aperture'] = 'f/' + get_meta_output(meta)
        elif 'ISO' in meta:
            meta_json['iso'] = get_meta_output(meta)
        elif 'Lens Info' in meta and len(args.lens) == 0:
            lens_info = get_meta_output(meta)
            if 'Fujifilm' in meta_json['camera']:
                if '56mm' in lens_info and '1.2' in lens_info:
                    meta_json['lens'] = 'Fujinon XF56mmf1.2'
                elif '23mm' in lens_info and '2' in lens_info:
                    meta_json['lens'] = 'Fujinon XF23mmf2'
                elif '35mm' in lens_info and '1.4' in lens_info:
                    meta_json['lens'] = 'Fujinon XF35mmf1.4'
                elif '50-230mm' in lens_info:
                    meta_json['lens'] = 'Fujinon XC50-230mmf4.5-6.7 II'
                elif '18-55mm' in lens_info:
                    meta_json['lens'] = 'Fujinon XF18-55mmf2.8-4'
                elif '27mm' in lens_info:
                    meta_json['lens'] = 'TTArtisan AF27mmf/2.8'
            elif 'Sony' in meta_json['camera']:
                if '35mm' in lens_info and '1.8' in lens_info:
                    meta_json['lens'] = 'FE35mmf1.8'
        elif 'Focal Length In 35mm Format' in meta and meta_json['camera'] == 'Xiaomi 13 Ultra':
            lens_info = get_meta_output(meta)
            meta_json['lens'] = lens_info + " (35mm equiv.)"
    print(json.dumps(meta_json, indent = 4)+',')


if __name__ == '__main__':
    main()
