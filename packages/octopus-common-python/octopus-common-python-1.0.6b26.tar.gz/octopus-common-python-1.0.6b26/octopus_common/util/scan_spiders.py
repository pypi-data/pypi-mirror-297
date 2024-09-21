import os
import inspect
import types

from octopus_common.constant.Constants import TASK_TYPE_FIELD_NAME
from octopus_common.model.Crawler import Crawler


def load_crawler_class(crawlers_directory, task_type):
    # 获取项目根目录的绝对路径
    project_root = os.path.abspath(os.getcwd())
    # 获取需要扫描的目录的绝对路径
    absolute_crawlers_directory = os.path.join(project_root, crawlers_directory)

    # 遍历目录下的所有文件
    for root, _, files in os.walk(absolute_crawlers_directory):
        for filename in files:
            crawler_name, _ = os.path.splitext(filename)
            if filename.endswith('.py') and filename != '__init__.py':
                dynamic_module = types.ModuleType('dynamic_module')

                with open(f'{root}//{filename}', 'r', encoding='utf-8', ) as file:
                    extension = file.read()
                # 在新模块的命名空间中执行代码
                exec(extension, dynamic_module.__dict__)

                for name, obj in dynamic_module.__dict__.items():
                    if inspect.isclass(obj) and issubclass(obj, Crawler) and obj != Crawler:
                        crawler_class = obj()
                        if hasattr(crawler_class, TASK_TYPE_FIELD_NAME):
                            task_types = getattr(crawler_class, TASK_TYPE_FIELD_NAME)
                            if task_type in task_types:
                                return crawler_class
