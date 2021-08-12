import shlex
import subprocess
from os import listdir
from os.path import isfile, join


def run_command(command):
    try:
        process = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT, timeout=90)
    except:
        pass
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        elif output.__contains__('not found'):
            print('Error, command not found \n {}'.format(output))
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
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    return onlyfiles


def get_lines_in_file(file):
    file1 = open(file, 'r')
    Lines = file1.readlines()
    return [line for line in Lines]
