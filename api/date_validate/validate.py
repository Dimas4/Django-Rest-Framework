from datetime import datetime
from .exception.exception import EmployeeWorkError, EmployeeStartWorkError, EmployeeEndWorkError


class Validate:
    @classmethod
    def _from_date_to_datetime(cls, date):
        return datetime(
            year=date.year,
            month=date.month,
            day=1,
        )

    @classmethod
    def _validate_work_start(cls, work_start_dt, datetime_object):
        work_start_datetime = cls._from_date_to_datetime(work_start_dt)

        if not datetime_object >= work_start_datetime:
            raise EmployeeStartWorkError

    @classmethod
    def _validate_work_end(cls, work_end_dt, datetime_object):
        if work_end_dt:
            work_end_datetime = cls._from_date_to_datetime(work_end_dt)

            if not datetime_object <= work_end_datetime:
                raise EmployeeEndWorkError

    @classmethod
    def validate_employee_work(cls, work_start_dt, work_end_dt, datetime_object):
        try:
            cls._validate_work_start(work_start_dt, datetime_object)
            cls._validate_work_end(work_end_dt, datetime_object)
        except (EmployeeStartWorkError, EmployeeEndWorkError):
            raise EmployeeWorkError
