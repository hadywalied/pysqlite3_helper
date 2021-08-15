class SAHandler:
    pk_values = ['CGMII']

    def __init__(self, db):
        self.db = db
        table_name = 'SA'
        primary_key = 'speed'
        self.exact_values = []
        self.get_exact_values_list(primary_key, table_name)

    def get_exact_values_list(self, primary_key, table_name):
        for pk_value in self.pk_values:
            self.exact_values.append(self.db.get_elements_subject_to_col(table_name, primary_key, pk_value))

    def return_expected_consumption(self):
        consumption = len(self.exact_values) * [0]
        for i, exact_value in enumerate(self.exact_values):
            for value in exact_value.items():
                if value[0] != 'speed' and value[0] != 'tolerance':
                    consumption[i] = consumption[i] + value[1]
        return consumption

    def get_tolerance(self):
        tolerance = len(self.exact_values) * [0]
        for i, exact_value in enumerate(self.exact_values):
            tolerance[i] = exact_value['tolerance']
        return tolerance
