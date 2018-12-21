def clear_database(*args):
    """
    Clears the database tables

    :param args: database tables
    :return: None
    """
    for model in args:
        model.objects.all().delete()
