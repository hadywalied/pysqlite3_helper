import shlex
import subprocess
from os import listdir
from os.path import isfile, join


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            yield output
    #         if output.__contains__('EPGM'):
    #             print(output.strip())
    #         elif output.__contains__('error'):
    #             rc = -1
    #             return rc
    # rc = process.poll()
    # return rc


def get_files_in_directory(directory: str):
    onlyfiles = [f for f in listdir(f'{directory}') if isfile(join(f'{directory}', f))]
    return onlyfiles


def get_lines_in_file(file):
    file1 = open(f'{file}', 'r')
    Lines = file1.readlines()
    return [line for line in Lines]