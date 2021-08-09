from os import listdir
from os.path import isfile, join
import subprocess
import shlex
import math


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
                print(output.strip())

            # if output.__contains__('EPGM'):
            # elif output.__contains__('error'):
            #     rc = -1
            #     return rc
    rc = process.poll()
    return rc

if __name__ == "__main__":
    run_command('winget --version')