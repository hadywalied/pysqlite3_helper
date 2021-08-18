class SAHandler:
    pk_values = ['CGMII']

    def __init__(self, db):
        '''initialize the SA Table Handler'''
        self.db = db
        table_name = 'SA'
        primary_key = 'speed'
        self.exact_values = []
        self.get_exact_values_list(primary_key, table_name)

    def get_exact_values_list(self, primary_key, table_name):
        """get the exact values from the db"""
        for pk_value in self.pk_values:
            self.exact_values.append(self.db.get_elements_subject_to_col(table_name, primary_key, pk_value))

    def return_expected_consumption(self):
        """calculate the expected consumption"""
        consumption = len(self.exact_values) * [0]
        for i, exact_value in enumerate(self.exact_values):
            for value in exact_value[0].items():
                if value[0] != 'speed' and value[0] != 'tolerance':
                    consumption[i] = consumption[i] + value[1]
        return consumption

    def get_tolerance(self):
        """get the tolerance field"""
        tolerance = len(self.exact_values) * [0]
        for i, exact_value in enumerate(self.exact_values):
            tolerance[i] = exact_value[0]['tolerance']
        return tolerance
