import asyncio
import pdb
import time
from os import environ

from src.Database.setup.FiveG.FiveG_helper import FiveGHelper
from src.Database.setup.Ethernet.ethrenet_helper import EthernetHelper

import subprocess
import sys

from src.core.handlers.handlers import Handler
from src.core.observers import ConcreteSubject, ConcreteObserverA
from src.core.utils import run_command, get_files_in_directory, get_lines_in_file, scrub


# sys.path.insert(1, environ['STAMP_REG_PATH'] + '/Common/python/')


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
                *iterates over DUT instances and get expected memory from the Database file specified for this instance
                        and sum all of them to get total expected consumption *
    '''

    def __init__(self, instance):

        application_name = instance["application"].lower()
        self.logging_path = instance["logging_dir"]
        self.py_ver = instance["python_version"]

        if application_name == '5g':
            self.db_helper = FiveGHelper()
            self.app = 0  # 0 --> 5G
            self.usage_path = ''
        elif application_name == 'ethernet':
            self.db_helper = EthernetHelper()
            self.app = 1  # 1 --> ethernet
            self.usage_path = '/project/med/Ethernet/EngineeringBuilds/VirtualEthernet_v11.3.1_b4126/userware/utilities/vvedusage.sh'
        else:
            print('There is a problem with the application_name, it can only be ethernet or 5g, eth is the default')
            self.db_helper = EthernetHelper()
            self.app = 0  # 1 --> ethernet
            self.usage_path = '/project/med/Ethernet/EngineeringBuilds/VirtualEthernet_v11.3.1_b4126/userware/utilities/vvedusage.sh'

        self.instances_list = instance['instances']  # keep track of the DUT instance

        self.db_handler = Handler(instances_list=self.instances_list, db=self.db_helper)
        # self.expected_data = self.db_handler.calculate_consumption()

        self.tracker_path_ = instance["tracker_path"]

        self.processes = {}

        self.subject = ConcreteSubject()
        self.observer_a = ConcreteObserverA()
        self.subject.attach(self.observer_a)

        self.initialize_consumption(self.tracker_path_)

    def initialize_consumption(self, tracker_path):
        command = "bash {tracker_path} {usage_path} {logging_path} {py_ver} {app}".format(
            tracker_path=tracker_path, usage_path=self.usage_path, logging_path=self.logging_path,
            py_ver=self.py_ver, app=self.app)
        self.subject.start_process(command)

    def main(self):
        self.analyze_log_files()
        self.validate_consumption(self.processes)

    def analyze_log_files(self):
        log_files_list = get_files_in_directory(self.logging_path)
        self.analyze_memory_files(self.logging_path, log_files_list)

    def analyze_memory_files(self, logging_path, log_files_list):
        memory_files = [file for file in log_files_list if 'memory_' in file]
        # pdb.set_trace()
        for file in memory_files:
            lines = get_lines_in_file(logging_path + '/' + file)
            if (len(lines) < 2):
                time.sleep(30)
                lines = get_lines_in_file(logging_path + '/' + file)
                if (len(lines) < 2):
                    print("error in log file {}".format(file))
                    sys.exit(0)

            process_id = scrub(lines[0].split(' ')[-1])
            memories = []
            process_name = scrub(str(lines[0].split(',')[0].split(':')[1]))
            for i in lines[1:]:
                x = i.split(' ')
                memories.append(int(x[-2]))
            self.processes[
                '{process_name}_{process_id}'.format(process_name=process_name, process_id=process_id)] = tuple(
                [memories[0], max(memories)])

    def validate_consumption(self, processes):
        # pdb.set_trace()
        self.memory_info_dict = {}
        for i, process in enumerate(processes.items()):
            process_name, process_id = process[0].split('_')[0], process[0].split('_')[1]
            initial_consumption = process[1][0]
            expected_memory_consumption = 0
            expected_memory_consumption = self.calculate_expected_value(expected_memory_consumption,
                                                                        initial_consumption, process)
            actual_memory_consumption = process[1][1]
            tolerance_ratio = self.get_tolerance() + 1
            if actual_memory_consumption > tolerance_ratio * expected_memory_consumption:
                no_leakage, log_message, memory_leakage, actual_memory_consumption, process_name, process_id = self.report_excessive_consumption(
                    actual_memory_consumption, expected_memory_consumption, process_name,
                    process_id)
                self.memory_info_dict["memory_{}.log".format(process_id).replace('.', '_')] = {'no_leakage': no_leakage,
                                                                                               'log_message': log_message,
                                                                                               'memory_leakage': memory_leakage,
                                                                                               'actual_memory_consumption': actual_memory_consumption,
                                                                                               'running_process':
                                                                                                   process[0]}
            else:
                no_leakage, log_message, memory_leakage, actual_memory_consumption, process_name, process_id = self.report_regular_consumption(
                    actual_memory_consumption, expected_memory_consumption, process_name,
                    process_id)
                self.memory_info_dict["memory_{}.log".format(process_id).replace('.', '_')] = {'no_leakage': no_leakage,
                                                                                               'log_message': log_message,
                                                                                               'memory_leakage': memory_leakage,
                                                                                               'actual_memory_consumption': actual_memory_consumption,
                                                                                               'running_process':
                                                                                                   process[0]}
        print("memory_info_dict", self.memory_info_dict)

    def calculate_expected_value(self, expected_memory_consumption, initial_consumption, process):
        # pdb.set_trace()
        total_accumulated_consumptions = self.db_handler.calculate_consumption(key=process[0])
        for total_accumulated_consumption in total_accumulated_consumptions:
            expected_memory_consumption = expected_memory_consumption + sum(total_accumulated_consumption)
        expected_memory_consumption = expected_memory_consumption + initial_consumption
        return expected_memory_consumption

    def get_tolerance(self):
        tolerance = []
        for t in self.db_handler.get_tolerance():
            tolerance.append(max(t))
        return max(tolerance)

    def report_excessive_consumption(self, actual_memory_consumption, expected_memory_consumption, process_name,
                                     process_number):
        memory_leakage = actual_memory_consumption - expected_memory_consumption
        log_message = "Memory leakage detected in " + process_name + ' in the memory logging file: \"' + 'memory_' + process_number + '\".'
        log_message += ' Actual Memory Consumption = ' + str(
            actual_memory_consumption) + 'MB. Expected memory consumption = ' + str(expected_memory_consumption) + 'MB.'
        log_message += ' Memory leakage value = ' + str(memory_leakage) + 'MB.'
        no_leakage = False
        return no_leakage, log_message, memory_leakage, actual_memory_consumption, process_name, process_number
        # print('exccessive usage')

    def report_regular_consumption(self, actual_memory_consumption, expected_memory_consumption, process_name,
                                   process_number):
        no_leakage = True
        log_message = "No Memory leakage detected in " + process_name + ' in the memory logging file: \"' + 'memory_' + process_number + '\".'
        log_message += ' Actual Memory Consumption = ' + str(
            actual_memory_consumption) + 'MB. Expected memory consumption = ' + str(expected_memory_consumption) + 'MB.'
        memory_leakage = 0
        return no_leakage, log_message, memory_leakage, actual_memory_consumption, process_name, process_number
        # print('regular usage')

    def __del__(self):
        self.subject.detach(self.observer_a)


if __name__ == "__main__":
    pass
