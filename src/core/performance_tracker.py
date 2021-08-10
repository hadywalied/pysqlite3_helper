from src.DB.database_playground import EthernetHelper, EthgHelper

# try:
#     import __builtin__
# except:
#     import builtins as __builtin__

import subprocess
import json

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
                *iterates over DUT instances and get expected memory from the DB file specified for this instance
                        and sum all of them to get total expected consumption *
    '''

    def __init__(self, instance):
        '''define instances_dict as follows :
            instances_dict = {
                "SA": ["CGMII", "CGMII"],
	            "MPG":{1:["CGMII, 12, 13],
			           2:[21, 22, 23]},
	            "veFlex":{1:{1:[15, 16],2:[17,18]}}
            }
            instances_dict = {
            "table_name" : e.g. SA
            "PK" :  e.g. speeds
            "value" : e.g. CGMII,
            "is_streaming":e.g. True
            "macs_numbers_id" :  [] #ports
            }

            logging_path = './logs'
            python_version : (2 for python2, 3 for python3)
        '''
        application_name = instance["application"].lower()
        self.logging_path = instance["logging_dir"]
        self.py_ver = instance["python_version"]

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

        self.instances_list = instance['instances']  # keep track of the DUT instance

        # table_name = self.instances_dict['DUT'].upper()
        # primary_key = self.instances_dict['key']
        # value = self.instances_dict['value']

        # self.expected_data = self.db_helper.get_elements_subject_to_col(table_name, primary_key, value)

        self.db_handler = Handler(instances_list=self.instances_list, db=self.db_helper)
        self.expected_data = self.db_handler.calculate_consumption()

        tracker_path_ = instance["tracker_path"]

        self.processes = {-1: tuple([0, 0])}
        self.initialize_consumption(tracker_path_)

    def initialize_consumption(self, tracker_path):
        # first line is the initial consumption
        self.problem_flag = False
        try:
            for output in run_command(
                    f'bash {tracker_path} {self.usage_path} {self.logging_path} {self.py_ver} {self.app}'):
                if output.__contains__('EPGM'):
                    print(output.strip())
                elif output.__contains__('error'):
                    print(f'something went wrong: {output}')
                    self.problem_flag = True
        except subprocess.CalledProcessError as e:
            print(e.output)

    def handle_command_output(self):
        if self.problem_flag:
            self.processes[-1] = tuple([-1, -1])
            return
        # if rc != -1:
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
            self.processes[process_id] = tuple([memories[0], max(memories)])

    def validate_consumption(self, processes):
        for i, process in enumerate([v for k, v in processes.items()]):
            if process[0] == -1:
                print("error")
                break
            elif process[0] == 0:
                continue
            initial_consumption = process[0]
            consumptions = self.db_handler.calculate_consumption()
            expected = consumptions[i] + initial_consumption
            actual = process[1]
            tolerance_ratio = self.get_tolerance()[i] + 1
            if (actual > tolerance_ratio * expected):
                self.report_excessive_consumption()
            else:
                pass

    def get_tolerance(self):
        return list(self.db_handler.get_tolerance())

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
    '''instances_ex = {
        "SA": ["CGMII", "CGMII"],
        "MPG": {1: ["CGMII", 12, 13],
                2: [21, 22, 23]},
        "veFlex": {1: {1: [15, 16], 2: [17, 18]}}
    }'''
    json_text = open('../input_configuration.json', 'r')
    instance = json.load(json_text)
    # instances = {'table_name': 'SA', 'PK': 'speed', 'value': 'CGMII', 'is_streaming': True}
    tracker = PerformanceTracker(instance)
