#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024-04-28 19:01:34
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   任务服务模块
'''

from typing import Callable
import pkgutil
from importlib import import_module
import uuid

from PySide6.QtCore import Slot

from .ts_item import TSItem
from .tasks import Tasks
from .task_base import TaskBase
from .service_base import ServiceBase
from .services import Services
from ..model import Result, Request


class TS:
    tasks = Tasks
    service = Services
    callback = {}

    @classmethod
    def add(cls, tsItme: TSItem):
        cls.tasks.append_Task(tsItme)
        cls.service.add_service(tsItme)

    @classmethod
    def get_all_task_names(cls) -> list:
        task_names_list = []
        for task_name, task_class in cls.tasks.TaskClasses.items():
            task_names_list.append(task_name)
        return task_names_list
    
    @classmethod
    def append_callback(cls, id, func):
        cls.callback[id] = func

    @classmethod
    def delete_callback(cls, id):
        try:
            del cls.callback[id]

        except KeyError:
            raise ValueError(f"Callback with id {id} not found.")
            
    @classmethod
    def send_data(cls, task_name:str, args:dict, callback=None):
        try:
            id = str(uuid.uuid4())
            service = cls.service.get_service(task_name, callback)
            request = Request(id=id, task_name=task_name, args=args)
            cls.append_callback(request.id, service.callback)
            service.request(request)
        except Exception as e:
            raise ValueError(f"Task {task_name} not found. {e}")

    @Slot(dict)
    @classmethod
    def on_client_connected(cls, response_data_dict: dict):
        if "task_name" not in response_data_dict or "id" not in response_data_dict:
            raise ValueError("Response data must contain 'task_name' and 'id'.")
        try:
            response = Result.model_validate(response_data_dict)
        except Exception as e:
            raise ValueError(response_data_dict)
        try:
            cls.callback.get(response.id)(response) # type: ignore
        except KeyError:
            raise ValueError(f"Callback with id {response.id} not found.")
        cls.delete_callback(response.id)


def create_ts_item(task_func: Callable) -> TSItem:
    class DynamicService(ServiceBase):
        TASK_NAME = f"{task_func.__name__}"
        def __init__(self, callback_func, task_name=TASK_NAME):
            self.callback_func = callback_func
            super(DynamicService, self).__init__(task_name)

    class DynamicTask(TaskBase):
        TASK_NAME = "{task_func.__name__}"
        def __init__(self, id: str, params: dict):
            super(DynamicTask, self).__init__(task_func.__name__, id, params)
            self.task = task_func
    return TSItem(task_func.__name__, DynamicTask, DynamicService)


def task_function(func: Callable):
    func.is_task = True
    return func


def discover_and_mount_ts_item(base_package: str):
    package = import_module(base_package)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
        module = import_module(module_name)
        for name, obj in vars(module).items():
            if callable(obj) and hasattr(obj, 'is_task'):
                ts_item = create_ts_item(obj)
                TS.add(ts_item)
    return TS, TS.send_data
