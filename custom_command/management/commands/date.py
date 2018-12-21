import random

from datetime import date

from faker import Faker


class Date:
    faker = Faker()

    @classmethod
    def convert_to_first_day(cls, date_):
        """
        Converts a date object to a date with a day of 1

        Example:
            input -> date(year=2015, month=12, day=5)
            output -> date(year=2015, month=12, day=1)

        :param date_: date object
        :return: date object
        """
        return date(year=date_.year, month=date_.month, day=1)

    @classmethod
    def random_date_from_obj(cls, start, end):
        """
        Creates new date objects between the start and end date using faker

        :param start: date object
        :param end: date object or None
        :return: date object
        """
        return cls.faker.date_between(
            start_date=start,
            end_date=end if end else "today"
        )

    @classmethod
    def generate_date_or_none(cls, month=(1, 12), year=(2018, 2018), count=50):
        """
        Creates a list (len equals count) with date objects at a specified
        interval (year, month) and day equal to 1

        :param month: tuple(start, end)
        :param year: tuple(start, end)
        :param count: objects count
        :return: list()
                 type(list[0]) -> date object
        """

        return [random.choice([date(
                    year=random.randint(*year),
                    month=random.randint(*month),
                    day=1
                ), None]
            ) for _ in range(count)
        ]
