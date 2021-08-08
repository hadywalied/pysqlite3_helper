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


# sys.path.insert(1, environ['STAMP_REG_PATH'] + '/Common/python/')


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

    def __init__(self, application_name: str, instances_dict: dict, usage_detiction_path, logging_path: str,
                 python_version: str):
        if application_name == 'ethg':
            self.db_helper = EthgHelper()
            self.app = 0  # 0 --> 5G
        elif application_name == 'eth':
            self.db_helper = EthernetHelper()
            self.app = 0  # 1 --> thernet
        else:
            print('There is a problem with the application_name, it can only be eth or ethg, eth is the default')
            self.db_helper = EthernetHelper()
            self.app = 0  # 1 --> thernet

        self.instances_dict = instances_dict  # keep track of the DUT instance
        self.expected_data = self.db_helper.get_elements_subject_to_col(self.instances_dict['table_name'],
                                                                        self.instances_dict['type'],
                                                                        self.instances_dict['speed'])
        self.logging_path = logging_path
        self.py_ver = python_version
        self.initialize_consumption()

    def initialize_consumption(self,
                               vvedusage_path='/project/med/Ethernet/EngineeringBuilds/VirtualEthernet_v11.3.1_b4126/userware/utilities/vvedusage.sh'):

        # vvedusage_process = subprocess.run(["bash", vvedusage_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                    universal_newlines=True)
        try:
            tracker_process = subprocess.run(
                ["bash", "track-memory-dut-gui.sh", vvedusage_path, self.logging_path, self.py_ver, self.app],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True
            )
        except subprocess.CalledProcessError as e:
            print(e.output)

    def validate_consumption(self):
        expected = self.calculate_expected_consumption()
        actual = self.calculate_actual_consumption()
        tolerance_ratio = 1.1
        if (actual > tolerance_ratio * expected):
            self.report_excessive_consumption()
        else:
            pass

    def calculate_expected_consumption(self):
        pass

    def calculate_actual_consumption(self):
        pass

    def report_excessive_consumption(self):
        pass

    def main(self):
        pass


if __name__ == "__main__":
    # print(get_files_in_directory('.'))
    # files = get_files_in_directory('.')
    # file = [file for file in files if 'memory_' in file]
    # print(get_lines_in_file(file[0]))
    print('working on it')
