#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tasks.py
@Time    :   2024-08-16 13:50:45
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   tasks
'''

from .ts_item import TSItem
from ..model import Request

class Tasks():
    TaskClasses = {}

    @classmethod
    def append_Task(cls, tsItme:TSItem):
        cls.TaskClasses[tsItme.TASK_NAME] = tsItme.task_class

    @classmethod
    def run_task(cls, request:Request):
        task_name = request.task_name
        TaskClass = cls.TaskClasses.get(task_name, lambda args: {
            "task_name": task_name, 
            "msg": "Task not found",
            "params": request
        })
        result = TaskClass(id=request.id, params=request.args).result_callback() if request.args is not None else TaskClass().result_callback() # type: ignore
        return result
    