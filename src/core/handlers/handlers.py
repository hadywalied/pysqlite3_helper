import pdb

from src.Database.setup.Ethernet.ethrenet_helper import EthernetHelper
from src.core.handlers.MPG_handler import MPGHandler
from src.core.handlers.SA_handler import SAHandler


class Handler:
    instances_list = []

    def __init__(self, instances_list, db):
        '''initializing the adapters with the db instance to calculate the consumption independently'''
        self.consumptions = []
        self.instances_list = instances_list
        self.db = db
        self.adapters = {
            'sa': DutAdapter(SAHandler(self.db), calculate_consumption='return_expected_consumption',
                             get_tolerance='get_tolerance'),
            # 'mpg': DutAdapter(MPGHandler(self.db), calculate_consumption='return_expected_consumption',
            #                   get_tolerance="get_tolerance")
        }

    def calculate_consumption(self, key):
        '''calculate the consumption based on the tool'''
        if key.__contains__('epgm'):
            # move logic inside the specific_handler
            self.calculate_expected_epgm_consumption()
        elif key.__contains__('controller'):
            # controller
            self.calculate_expected_epgm_consumption()  # TODO: replace this with the controller one
        else:
            # DUT
            self.calculate_expected_epgm_consumption()  # TODO: replace this with the DUT one

        return self.consumptions

    def calculate_expected_epgm_consumption(self):
        '''calculate the expected epgm consumption'''
        for instance in self.instances_list:
            adapter = self.adapters[instance['DUT'].lower()]
            adapter.pk_values = instance['value']
            self.consumptions.append(adapter.calculate_consumption())

    def get_tolerance(self):
        '''calculate the expected tolerance consumption'''
        self.tolerances = []
        for instance in self.instances_list:
            adapter = self.adapters[instance['DUT'].lower()]
            adapter.pk_value = instance['value']
            self.tolerances.append(adapter.get_tolerance())
            # yield adapter.calculate_consumption()
        return self.tolerances


class DutAdapter:
    _initialized = False

    def __init__(self, dut, **adapted_methods):
        self.dut = dut

        for key, value in adapted_methods.items():
            func = getattr(self.dut, value)
            self.__setattr__(key, func)

        self._initialized = True

    def __setattr__(self, key, value):
        """Set attributes normally during initialisation"""
        if not self._initialized:
            super().__setattr__(key, value)
        else:
            """Set attributes on DUT after initialisation"""
            setattr(self.dut, key, value)


if __name__ == "__main__":
    adapter = DutAdapter(SAHandler(EthernetHelper()), calculate_consumption='return_expected_consumption',
                         get_tolerance='get_tolerance')
    print(adapter.get_tolerance())
