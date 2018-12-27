class SalaryParamsError(Exception):
    def __init__(self, errors):
        self.errors = errors


class WorkDateError(Exception):
    def __init__(self, errors):
        self.errors = errors
