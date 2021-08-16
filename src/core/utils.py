import asyncio
import concurrent.futures
import os
import shlex
from os import listdir
from os.path import isfile, join
from threading import Timer
import time

import subprocess, threading

def scrub(name):
    return ''.join(ch for ch in name if ch.isalnum())

@asyncio.coroutine
def run_command(command):
    process = asyncio.subprocess.Popen(shlex.split(command), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            return output
        yield from asyncio.sleep(1)


def get_files_in_directory(directory: str):
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    return onlyfiles


def get_lines_in_file(file):
    file1 = open(file, 'r')
    Lines = file1.readlines()
    return [line for line in Lines]


@asyncio.coroutine
def pathmonitor(path):
    modtime = os.path.getmtime(path)
    while True:
        new_time = os.path.getmtime(path)
        if new_time != modtime:
            modtime = new_time
            return modtime
        yield from asyncio.sleep(1)


@asyncio.coroutine
def printer():
    while True:
        modtime = yield from pathmonitor('C:\\Users\\himep\\PycharmProjects\\pythonProject2\\test.txt')
        print(modtime)


if __name__ == "__main__":
    # command = Command("echo 'Process started'; sleep 2; echo 'Process finished'")
    # command.run(1)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future = executor.submit(foo, 'world!')
    #     for return_value in future.result():
    #         print(return_value)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(printer())
    loop.run_forever()
