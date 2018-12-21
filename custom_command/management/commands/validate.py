class Validate:
    @classmethod
    def is_none(cls, *args):
        for _param in args:
            if _param is None:
                raise ValueError

    @classmethod
    def validate(cls, *args):
        cls.is_none(*args)
