from .exception import NoneValueError


class Validate:
    @classmethod
    def is_none(cls, *args):
        for param in args:
            if param is None:
                raise NoneValueError

    @classmethod
    def validate(cls, company_count, employees_count):
        cls.is_none(company_count, employees_count)
