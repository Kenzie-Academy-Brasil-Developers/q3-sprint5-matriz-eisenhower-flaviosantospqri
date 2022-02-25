class InvalidDataError(Exception):
    ...


class NumberNotValid(Exception):
    valid_options = {'importance': [1, 2], 'urgency': [1, 2]}

    def __init__(self, importance, urgency):
        recieved_options = {'importance': importance, 'urgency': urgency}

        self.message = [
            {
                'valid_options': self.valid_options,
                'recieved_options': recieved_options

            }
        ]
        super().__init__(self.message)
