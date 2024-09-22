#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   services.py
@Time    :   2024-08-16 13:50:17
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   services
'''

# from .service_base import ServiceBase
from .ts_item import TSItem


class Services:
    services = {}

    @classmethod
    def add_service(cls, tsItme:TSItem):
        cls.services[tsItme.TASK_NAME] = tsItme.service_class

    @classmethod
    def get_service(cls, name, callback=None):   
        service_class = cls.services.get(name)  
        if service_class is None:  
            raise KeyError(f"Service '{name}' not found.")  
        if callback is not None:
            return service_class(callback)
        else:
            return service_class
        