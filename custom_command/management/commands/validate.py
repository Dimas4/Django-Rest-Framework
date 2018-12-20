from .exception import NoneValueError, LengthObjectError


class Validate:
    @classmethod
    def is_none(cls, *args):
        for param in args:
            if param is None:
                raise NoneValueError

    @classmethod
    def is_instance(cls, type_, *args):
        for obj in args:
            if not isinstance(obj, type_):
                raise TypeError

    @classmethod
    def is_correct_len(cls, len_, *args):
        for obj, obj_required_len in zip(args, len_):
            if len(obj) != obj_required_len:
                raise LengthObjectError

    @classmethod
    def validate(cls, company_count, employees_count, type_, len_):
        cls.is_none(company_count, employees_count)
        cls.is_instance(type_, company_count, employees_count)
        cls.is_correct_len(len_, company_count, employees_count)
