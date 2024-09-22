#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   service_item.py
@Time    :   2024-04-28 18:55:18
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   Service 父类
'''

from ..utils import client_send_request  
from ..model import Result, Request
import logging


class ServiceBase:

    def __init__(self, task_name):
        self.task_name = task_name

    def request(self, request: Request):
        client_send_request(request)

    def callback(self, result: Result):
        try:
            logging.info(f"{self.task_name} callback result: \n{result}")
            self.callback_func(result)
            
        except Exception as e:
            # print(f"{self.task_name} callback error: {e}")
            logging.error(f"{self.task_name} callback error: \n{e}")
            raise ValueError(f"{self.task_name} callback error: {e}")

    def callback_func(self, data):
        pass
    