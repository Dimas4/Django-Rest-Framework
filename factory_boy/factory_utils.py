import random

from datetime import date


def clear_database(*args):
    for model in args:
        model.objects.all().delete()


def generate_objects(count, obj, many=True, **kwargs):
    if many:
        return [obj(**kwargs) for _ in range(count)]
    return obj(**kwargs)


def generate_date_or_none():
    return [random.choice([date(
                year=2018,
                month=random.randint(1, 12),
                day=1
            ), None]
        ) for _ in range(50)
    ]
