from octopus_common.constant.Constants import TASK_TYPE_FIELD_NAME


def task_type(*task_types):
    def decorator(func):
        setattr(func, TASK_TYPE_FIELD_NAME, task_types)
        return func

    return decorator
