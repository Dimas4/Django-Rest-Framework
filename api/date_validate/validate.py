from datetime import datetime
from .exception.exception import EmployeeStartWorkError, EmployeeEndWorkError


class Validate:
    @classmethod
    def validate_employee_work(cls, work_start_dt, work_end_dt, datetime_object):
        work_start_str = datetime(
            year=work_start_dt.year,
            month=work_start_dt.month,
            day=1,
        )

        if not datetime_object >= work_start_str:
            raise EmployeeStartWorkError

        if work_end_dt:
            work_end_datetime = datetime(
                year=work_end_dt.year,
                month=work_end_dt.month,
                day=1,
            )
            if not datetime_object <= work_end_datetime:
                raise EmployeeEndWorkError
