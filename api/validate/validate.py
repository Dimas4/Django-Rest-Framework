class Validate:
    @classmethod
    def validate_by_serializer(cls, serializer, exception, data):
        salary_serializer = serializer(data=data)
        if not salary_serializer.is_valid():
            raise exception(errors=salary_serializer.errors)
        return salary_serializer
