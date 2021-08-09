from src.core.handlers.MPG_handler import MPGHandler
from src.core.handlers.SA_handler import SAHandler


# from builtins import getattr

class Handler:
    instances_list = []

    def __init__(self, instances_list, db):
        ''' '''
        self.instances_list = instances_list
        self.db = db

    def calculate_consumption(self):
        consumption = []
        adapters = {
            'sa': DutAdapter(SAHandler(self.db), calculate_consumption='return_expected_consumption'),
            'mpg': DutAdapter(MPGHandler(self.db), calculate_consumption='return_expected_consumption')
        }
        for instance in self.instances_list:
            consumption.append(adapters[instance['DUT'].lower()].calculate_consumption())

        return consumption


class DutAdapter:
    _initialized = False

    def __init__(self, dut, **adapted_methods):
        self.dut = dut

        for key, value in adapted_methods.items():
            func = getattr(self.dut, value)
            self.__setattr__(key, func)

        self._initialized = True

    # def __getattr__(self, attr):
    #     """Attributes not in Adapter are delegated to the DUT"""
    #     return getattr(self.dut, attr)

    def __setattr__(self, key, value):
        """Set attributes normally during initialisation"""
        if not self._initialized:
            super().__setattr__(key, value)
        else:
            """Set attributes on DUT after initialisation"""
            setattr(self.dut, key, value)


if __name__ == "__main__":
    adapter = DutAdapter(SAHandler(), calc='main')
    adapter.calc()
