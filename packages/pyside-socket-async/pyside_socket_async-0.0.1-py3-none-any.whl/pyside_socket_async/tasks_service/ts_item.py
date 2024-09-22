#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ts_item.py
@Time    :   2024-08-16 13:51:02
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   task service item
'''

from .service_base import ServiceBase
from .task_base import TaskBase


class TSItem:
    def __init__(self, task_name:str, TaskClass: type[TaskBase], ServiceClass: type[ServiceBase]):
        self.task_class = TaskClass
        self.service_class = ServiceClass
        self.TASK_NAME = task_name
        