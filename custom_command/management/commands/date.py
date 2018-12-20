from datetime import date

from faker import Faker


class Date:
    faker = Faker()

    @classmethod
    def convert_to_first_day(cls, date_):
        return date(year=date_.year, month=date_.month, day=1)

    @classmethod
    def random_date_from_obj(cls, start, end):
        return cls.faker.date_between(
            start_date=start,
            end_date=end if end else "today"
        )
