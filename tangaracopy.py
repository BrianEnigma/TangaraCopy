#!/usr/bin/env python3

from config import FOLDERS, EXTENSIONS_COPY, EXTENSIONS_TRANSCODE, FFMPEG_GLOBAL_OPTIONS, FFMPEG_ENCODE_OPTIONS
import argparse
import os
import shutil
import subprocess

class ProgramOptions:
    def __init__(self):
        self.file_limit = None

def prepare_destination_folder(output:str) -> None:
    directory:str = os.path.dirname(output)
    if not os.path.exists(directory):
        print("Creating directory " + directory)
        os.makedirs(directory, exist_ok=True)

def copy_file(input:str, output:str) -> None:
    # Don't copy if it's already there.
    if os.path.exists(output) and os.path.isfile(output):
        print("Skipping copy of " + output + " (file exists)")
        return
    print("Copying " + input + " to " + output)
    prepare_destination_folder(output)
    shutil.copy(input, output)

def transcode_file(input: str, output: str) -> None:
    # Change output file extension to .mp3
    output = os.path.splitext(output)[0] + ".mp3"
    # Don't transcode if it's already there.
    if os.path.exists(output) and os.path.isfile(output):
        print("Skipping transcode of " + output + " (file exists)")
        return
    print("Transcoding " + output)
    prepare_destination_folder(output)
    command = ['ffmpeg']
    command.extend(FFMPEG_GLOBAL_OPTIONS)
    command.extend(['-i', input])
    command.extend(FFMPEG_ENCODE_OPTIONS)
    command.append('-y')
    command.append(output)
    subprocess.run(command)

def action_based_on_extension(filename:str) -> str:
    lower_filename:str = filename.lower()
    for ext in EXTENSIONS_COPY:
        if lower_filename.endswith(ext):
            return "copy"
    for ext in EXTENSIONS_TRANSCODE:
        if lower_filename.endswith(ext):
            return "transcode"
    return "skip"

def copy_transcode_file(input:str, output:str, count:int, limit) -> int:
    for file_name in os.listdir(input):
        full_file_name: str = os.path.abspath(os.path.join(input, file_name))
        full_output_file_name: str = os.path.abspath(os.path.join(output, file_name))
        # Skip dot files
        if file_name.startswith('.'):
            continue
        # Filter by type
        if os.path.isfile(full_file_name):
            action:str = action_based_on_extension(file_name)
            if action == "copy":
                copy_file(full_file_name, full_output_file_name)
                count += 1
            elif action == "transcode":
                transcode_file(full_file_name, full_output_file_name)
                count += 1
            else:
                print("Skipping " + full_output_file_name + " (extension not in config)")
            count += 1
        elif os.path.isdir(full_file_name):
            count = copy_transcode_file(full_file_name, full_output_file_name, count, limit)
        else:
            print("Skipping " + full_output_file_name + " (not a file or directory)")
        if limit is not None and count >= limit:
            break
    return count


def parse_arguments():
    result:ProgramOptions = ProgramOptions()
    parser = argparse.ArgumentParser(prog='tangaracopy')
    parser.add_argument('-c', '--count', type=int)
    args = parser.parse_args()
    result.file_limit = args.count
    return result

program_options = parse_arguments()
for source_folder in FOLDERS:
    destination_folder = FOLDERS[source_folder]
    copy_transcode_file(source_folder, destination_folder, 0, program_options.file_limit)
