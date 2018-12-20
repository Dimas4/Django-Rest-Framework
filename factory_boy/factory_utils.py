def clear_database(*args):
    for model in args:
        model.objects.all().delete()
