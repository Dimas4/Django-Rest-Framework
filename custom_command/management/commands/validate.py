class Validate:
    @classmethod
    def is_none(cls, *args):
        """
        Raises ValueError if the parameter is None in the args list
        :param args:
        :return: None or raise ValueError
        """
        for _param in args:
            if _param is None:
                raise ValueError

    @classmethod
    def validate(cls, *args):
        """
        Check *arg list
        :param args:
        :return: None or ValueError
        """
        cls.is_none(*args)
