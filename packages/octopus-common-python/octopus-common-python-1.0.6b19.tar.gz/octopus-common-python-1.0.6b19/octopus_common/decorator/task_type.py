def task_type(*task_types):
    def decorator(func):
        func.task_types = task_types
        return func

    return decorator
