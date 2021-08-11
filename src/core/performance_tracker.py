from src.Database.setup.FiveG.FiveG_helper import FiveGHelper
from src.Database.setup.Ethernet.ethrenet_helper import EthernetHelper


import subprocess
import sys
# sys.path.insert(1, environ['STAMP_REG_PATH'] + '/Common/python/')
from src.core.handlers.handlers import Handler
from utils import run_command, get_files_in_directory, get_lines_in_file


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
            print('There is a problem with the application_name, it can only be eth or ethg, eth is the default')
            self.db_helper = EthernetHelper()
            self.app = 0  # 1 --> ethernet
            self.usage_path = '/project/med/Ethernet/EngineeringBuilds/VirtualEthernet_v11.3.1_b4126/userware/utilities/vvedusage.sh'

        self.instances_list = instance['instances']  # keep track of the DUT instance

        self.db_handler = Handler(instances_list=self.instances_list, db=self.db_helper)
        self.expected_data = self.db_handler.calculate_consumption()

        tracker_path_ = instance["tracker_path"]

        self.processes = {}
        self.initialize_consumption(tracker_path_)

    def initialize_consumption(self, tracker_path):
        try:
            for output in run_command(
                    f'bash {tracker_path} {self.usage_path} {self.logging_path} {self.py_ver} {self.app}'):
                if output.__contains__('error'):
                    print(f'something went wrong: {output}')
                    self.problem_flag = True
                    sys.exit()
                print(output.strip())
        except subprocess.CalledProcessError as e:
            print(e.output)
            sys.exit()

    def main(self):
        if not self.problem_flag:
            self.analyze_log_files()
            self.validate_consumption(self.processes)

    def analyze_log_files(self):
        log_files_list = get_files_in_directory(self.logging_path)
        self.analyze_memory_files(log_files_list)

    def analyze_memory_files(self, log_files_list):
        memory_files = [file for file in log_files_list if 'memory_' in file]
        for file in memory_files:
            lines = get_lines_in_file(file)
            process_id = lines[0].split(' ')[-1]
            memories = []
            for file in memory_files:
                lines = get_lines_in_file(file)
                process_id = str(lines[0].split(' ')[-1])
                process_name = str(lines[0].split(',')[0].split(' ')[1])
                for i in lines[1:]:
                    x = i.split(' ')
                    memories.append(int(x[-2]))
                self.processes[f'{process_name}_{process_id}'] = tuple([memories[0], max(memories)])

    def validate_consumption(self, processes):
        for i, process in enumerate(processes.items()):
            initial_consumption = process[1][0]
            expected_memory_consumption = 0
            expected_memory_consumption = self.calculate_expected_value(expected_memory_consumption, i,
                                                                        initial_consumption, process)
            actual_memory_consumption = process[1][1]
            tolerance_ratio = self.get_tolerance() + 1
            if actual_memory_consumption > tolerance_ratio * expected_memory_consumption:
                self.report_excessive_consumption()
            else:
                self.report_regular_consumption()

    def calculate_expected_value(self, expected_memory_consumption, i, initial_consumption, process):
        total_accumulated_consumptions = self.db_handler.calculate_consumption(key=process[0])
        for j, total_accumulated_consumption in enumerate(total_accumulated_consumptions):
            expected_memory_consumption = expected_memory_consumption + sum(total_accumulated_consumption[i])
        expected_memory_consumption = expected_memory_consumption + initial_consumption
        return expected_memory_consumption

    def get_tolerance(self):
        tolerance = []
        for t in self.db_handler.get_tolerance():
            tolerance.append(max(t))
        return max(tolerance)

    def report_excessive_consumption(self):
        pass

    def report_regular_consumption(self):
        pass


if __name__ == "__main__":
    pass
