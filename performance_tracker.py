from database_playground import EthernetHelper, EthgHelper

# try:
#     import __builtin__
# except:
#     import builtins as __builtin__

import sys
from os import environ
from os import listdir
from os.path import isfile, join
import subprocess
import shlex
import math


# sys.path.insert(1, environ['STAMP_REG_PATH'] + '/Common/python/')


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            if output.__contains__('EPGM'):
                print(output.strip())
            elif output.__contains__('error'):
                rc = -1
                return rc
    rc = process.poll()
    return rc


def get_files_in_directory(directory: str):
    onlyfiles = [f for f in listdir(f'{directory}') if isfile(join(f'{directory}', f))]
    return onlyfiles


def get_lines_in_file(file):
    file1 = open(f'{file}', 'r')
    Lines = file1.readlines()
    return [line for line in Lines]


class PerformanceTracker:
    '''
    Class with the following specifications:
    Its constructor will store application_name and instances_list then will call "initialize_consumption()"
    initialize_consumption() is method to apply the following:
    refer to steps file
    validate_consumption() will apply the following:
        Iterates over memory log files
            For each file, check application name, if not exist then it's DUT logs
            Get largest memory consumption in file as actual memory consumption
            Get expected info based on DUT info
                *iterates over DUT instances and get expected memory from the DB file specified for this instance
                        and sum all of them to get total expected consumption *
    '''

    def __init__(self, application_name: str, instances_dict: dict, logging_path: str,
                 python_version: str):

        '''define instances_dict as follows :
            instances_dict = {
                "SA": ["CGMII", "CGMII"],
	            "MPG":{1:["CGMII, 12, 13],
			           2:[21, 22, 23]},
	            "veFlex":{1:{1:[15, 16],2:[17,18]}}
            }
            instances_dict = {
            "table_name" : e.g. SA
            "type" :  e.g. speeds
            "value" : e.g. CGMII
            "macs_numbers_id" :  [] #ports
            }

            logging_path = './logs'
            python_version : (2 for python2, 3 for python3)
        '''

        if application_name == 'ethg':
            self.db_helper = EthgHelper()
            self.app = 0  # 0 --> 5G
            self.usage_path = ''
        elif application_name == 'eth':
            self.db_helper = EthernetHelper()
            self.app = 1  # 1 --> ethernet
            self.usage_path = '/project/med/Ethernet/EngineeringBuilds/VirtualEthernet_v11.3.1_b4126/userware/utilities/vvedusage.sh'
        else:
            print('There is a problem with the application_name, it can only be eth or ethg, eth is the default')
            self.db_helper = EthernetHelper()
            self.app = 0  # 1 --> ethernet
            self.usage_path = '/project/med/Ethernet/EngineeringBuilds/VirtualEthernet_v11.3.1_b4126/userware/utilities/vvedusage.sh'

        self.instances_dict = instances_dict  # keep track of the DUT instance
        self.expected_data = self.db_helper.get_elements_subject_to_col(self.instances_dict['table_name'],
                                                                        self.instances_dict['type'],
                                                                        self.instances_dict['speed'])
        self.logging_path = logging_path
        self.py_ver = python_version
        self.processes = self.initialize_consumption()

    def initialize_consumption(self):

        # vvedusage_process = subprocess.run(["bash", vvedusage_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                    universal_newlines=True)
        # first line is the initial consumption
        rc = 1
        try:
            rc = run_command(
                f'bash track-memory-dut-gui.sh {self.usage_path} {self.logging_path} {self.py_ver} {self.app}')
            # tracker_process = subprocess.run(
            #     ["bash", "track-memory-dut-gui.sh", self.usage_path, self.logging_path, self.py_ver, self.app],
            #     stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True
            # )
        except subprocess.CalledProcessError as e:
            print(e.output)
        processes = self.handle_command_output(rc)
        return processes

    def handle_command_output(self, rc):
        processes = {-1: tuple(0, 0)}
        if rc != -1:
            log_files_list = get_files_in_directory(self.logging_path)
            memory_files = [file for file in log_files_list if 'memory_' in file]
            for file in memory_files:
                lines = get_lines_in_file(file)
                process_id = lines[0].split(' ')[-1]
                memories = []
                for file in memory_files:
                    lines = get_lines_in_file(file)
                    process_id = int(lines[0].split(' ')[-1])
                    for i in lines[1:]:
                        x = i.split(' ')
                        memories.append(int(x[-2]))
                processes[process_id] = tuple([memories[0], max(memories)])
        elif rc == -1:
            processes[-1] = tuple([-1, -1])
            print("something wrong has happened")
        else:
            pass
        return processes

    # self.initial_consumption =

    def validate_consumption(self, processes):
        for process in [v for k, v in processes.items()]:
            if (process[0] == -1 or process[0] == 0):
                continue
            initial_consumption = process[0]
            expected = self.calculate_expected_consumption() + initial_consumption
            actual = process[1]
            tolerance_ratio = self.get_tolerance() + 1
            if (actual > tolerance_ratio * expected):
                self.report_excessive_consumption()
            else:
                pass

    def get_tolerance(self):
        return int(self.expected_data['tolerance'])

    def calculate_expected_consumption(self):
        return self.expected_data['dc_memory_value'] + (
            self.expected_data['streaming_value'] if self.instances_dict['is_streaming'] == True else
            self.expected_data['memory_per_port'])

    def report_excessive_consumption(self):
        pass

    def main(self):
        self.validate_consumption(self.processes)


if __name__ == "__main__":
    # print(get_files_in_directory('.'))
    # files = get_files_in_directory('.')
    # file = [file for file in files if 'memory_' in file]
    # print(get_lines_in_file(file[0]))
    # print('working on it')
    instances_ex = {
        "SA": ["CGMII", "CGMII"],
        "MPG": {1: ["CGMII", 12, 13],
                2: [21, 22, 23]},
        "veFlex": {1: {1: [15, 16], 2: [17, 18]}}
    }
    instances = {"SA":}
    tracker = PerformanceTracker('eth', )
