from src.core.handlers.MPG_handler import MPGHandler
from src.core.handlers.SA_handler import SAHandler


class Handler:
    instances_list = []

    def __init__(self, instances_list, db):
        ''' '''
        self.consumptions = []
        self.instances_list = instances_list
        self.db = db
        self.adapters = {
            'sa': DutAdapter(SAHandler(self.db), calculate_consumption='return_expected_consumption',
                             get_tolerance='get_tolerance'),
            'mpg': DutAdapter(MPGHandler(self.db), calculate_consumption='return_expected_consumption',
                              get_tolerance="get_tolerance")
        }

    def calculate_consumption(self, key):
        if key.__contains__('EPGM'):
            # move logic inside the specific_handler
            self.calculate_expected_epgm_consumption()
        elif key.__contains__('controller'):
            pass
        else:
            # DUT
            pass

        return self.consumptions

    def calculate_expected_epgm_consumption(self):
        for instance in self.instances_list:
            adapter = self.adapters[instance['DUT'].lower()]
            adapter.pk_values = instance['value']
            self.consumptions.append(adapter.calculate_consumption())
            # yield adapter.calculate_consumption()

    def get_tolerance(self):
        self.tolerances = []
        for instance in self.instances_list:
            adapter = self.adapters[instance['DUT'].lower()].pk_value = instance['value']
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
