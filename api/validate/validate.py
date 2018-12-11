from api.serializers import SalaryParamsSerializer, WorkDateSerializer
from .exception.exception import SalaryParamsError, WorkDateError


class Validate:
    @classmethod
    def validate_salary_params(cls, data):
        salary_serializer = SalaryParamsSerializer(data=data)
        if not salary_serializer.is_valid():
            raise SalaryParamsError(errors=salary_serializer.errors)
        return salary_serializer

    @classmethod
    def validate_work_date(cls, data):
        work_date_serializer = WorkDateSerializer(data=data)
        if not work_date_serializer.is_valid():
            raise WorkDateError(errors=work_date_serializer.errors)
        return work_date_serializer
