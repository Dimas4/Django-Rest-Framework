from datetime import datetime

from .exception.exception import EmployeeWorkError, EmployeeStartWorkError, EmployeeEndWorkError


class Validate:
    @classmethod
    def _validate_work_start(cls, start_date, current_date):
        """
        Checks that current_date >= start_date

        :param start_date:
        :param current_date:
        :raise: EmployeeStartWorkError if current_date <= start_date
        """

        if not current_date >= start_date:
            raise EmployeeStartWorkError

    @classmethod
    def _validate_work_end(cls, end_date, current_date):
        """
        Checks that current_date <= end_date

        :param end_date:
        :param current_date:
        :raise: EmployeeEndWorkError if current_date >= end_date
        """
        if end_date:
            if not current_date <= end_date:
                raise EmployeeEndWorkError

    @classmethod
    def validate_date(cls, start_date, end_date, current_date):
        """
        Checks that start_date <= current_date <= end_date

        :param start_date:
        :param end_date:
        :param current_date:
        :raise: EmployeeWorkError if current_date <= start_date or current_date >= end_date
        """
        try:
            cls._validate_work_start(start_date, current_date)
            cls._validate_work_end(end_date, current_date)
        except (EmployeeStartWorkError, EmployeeEndWorkError):
            raise EmployeeWorkError
