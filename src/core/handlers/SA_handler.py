class SAHandler:
    pk_value = 'CGMII'

    def __init__(self, db):
        self.db = db
        table_name = 'SA'
        primary_key = 'speed'
        self.exact_values = self.db.get_elements_subject_to_col(table_name, primary_key, self.pk_value)

    def return_expected_consumption(self):
        consumption = 0
        for key, value in self.exact_values.items():
            if key != 'speed' and key != 'tolerance':
                consumption = consumption + value
        return consumption

    def get_tolerance(self):
        return self.exact_values['tolerance']
