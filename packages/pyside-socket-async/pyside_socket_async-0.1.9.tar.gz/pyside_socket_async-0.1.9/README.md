# PySide6 Socket 异步框架

作者：chakcy

简介：利用 socket、threding 和 Qt 插槽实现的异步通信框架。
仓库地址：https://gitee.com/cai-xinpenge/pyside_socket_async.git

## 目录

[TOC]

## 介绍

本框架旨在将运行时间较长的方法在一个线程中执行，最后通过插槽将结果返回给界面，其中涉及 socket 的通信，Qt多线程，Qt插槽，以及任务注册的概念。

## 主要实现思路

在开启 pyside 应用的同时启动另一个线程，该线程启动一个socket 服务，用于与界面进行交互。

在开启 socket 服务线程前，动态的检测某路径下的模块，将带有 @task_function 装饰器的方法动态的生成 TSItem类，并将它们添加到 TS 类的 services 和 tasks 中，tasks 会被初始化到 socket 线程中作为待调用的方法，而 services 则是主线程发送调用方法的指令，即但主线程调用 services 中的某个方法后，会向 socket 服务发送一个请求，该请求无需等待结果，socket 服务会开启一个线程调用对应的 task 方法，执行完成后，将结果通过插槽返回给主线程，TS 会通过某种机制将结果返回给对应 service 的回调函数。

## TS类的设计与回调管理

1. 回调函数的注册：
   - 在 TS 类中，有一个字典用于管理回调函数。每当主线程调用某个 service 的方法时，框架会生成一个唯一的标识符（UUID），作为字典中的键，将对应的回调函数作为值存入字典中。
   - 这种机制允许框架在执行任务时追踪每个请求和其对应的回调。
2. 任务执行与回调：
   - 当任务被发送到 socket 服务并执行时，服务会在任务执行完成后，构建一个结果对象，这个对象会包含之前生成的 UUID。
   - 框架使用 Qt 的插槽机制将结果发送回主线程。
3. 回调函数的调用：
   - 主线程接收到结果后，会利用结果中的 UUID 查询 TS 类中存储的字典，找到对应的回调函数。
   - 找到回调函数后，框架会执行该函数，并将结果传递给它。
4. 清理工作：
   - 在回调函数执行完毕后，框架会将字典中对应的键值对（即 UUID 和回调函数的对应关系）删除，一避免内存泄漏和保持字典的简洁。

## 依赖
```
pydantic>=2.9.1
PySide6>=6.7.2
requests>=2.32.3
colorlog>=6.8.2
```

## 使用案例

安装

```shell
mkdir demo
git clone https://gitee.com/cai-xinpenge/pyside_socket_async.git
cd pyside_socket_async
pip install .
```

目录结构

```
demo
├── app
│   ├── engine
│   │   ├── service
│   │   │   ├── __init__.py
│   │   │   └── test.py
│   │   ├── task
│   │   │   ├── __init__.py
│   │   │   └── test.py
│   │   └── __init__.py
│   ├── interface
│   │   ├── __init__.py
│   │   └── window.py
│   ├── views
│   │   ├── __init__.py
│   │   └── window.py
│   └── __init__.py
└── main.py
```



`main.py`

```python
import sys
from app import app, window_view

if __name__ == "__main__":
    window_view.show()
    sys.exit(app.exec())
```

`app/__init__.py`

```python
import sys

from PySide6 import QtWidgets
from pyside_socket_async.socket_thread import create_socket_server_thread

from .views import MainWindow
from .engine import task_service

app = QtWidgets.QApplication(sys.argv)
window_view = MainWindow()

create_socket_server_thread(task_service, app)


```

`app/engine/__init__.py`

```python
from pyside_socket_async.tasks_service import discover_and_mount_ts_item

task_service, send_data = discover_and_mount_ts_item('app.engine.task')
print(task_service.get_all_task_names())
```

`app/engine/service/__init__.py`

```python
from .test import TestService 


__all__ = ['TestService']
```

`app/engine/service/test.py`

```python
from typing import Union, Any

from app.engine import send_data
from app.interface import MainWindowInterface


class TestService:
    @classmethod
    def request(cls, data: dict, window:Union[MainWindowInterface, Any]):
        cls.window = window
        send_data("test", data, cls.callback)
    
    @classmethod
    def callback(cls, response):
        print(f"返回结果为：{response.result}")
        cls.window.pushButton.setText(f"{response.result}")

```

`app/engine/task/__init__.py`

```python
from .test import test


__all__ = ['test']

```

`app/engine/task/test.py`

```python
import time
from pyside_socket_async.tasks_service import task_function


@task_function
def test(args):
    time.sleep(5)
    a = 1 / 0
    return "test"

```

`app/interface/__init__.py`

```python
from .window import MainWindowInterface


__all__ = ["MainWindowInterface"]

```

`app/interface/window.py`

```python
from PySide6.QtWidgets import QPushButton


class MainWindowInterface:
    def __init__(self):
        self.pushButton: QPushButton

```

`app/views/__init__.py`

```python
from .window import MainWindow


__all__ = ["MainWindow"]

```

`app/views/window.py`

```python
from PySide6.QtWidgets import QPushButton, QMainWindow, QWidget

from ..engine.service import TestService


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.centralwidget = QWidget(self)
        self.init_ui()
        self.bind()

    def init_ui(self):
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setText("点击我")

    def bind(self):
        self.pushButton.clicked.connect(self.test)
    
    def test(self):
        TestService().request({}, self)

```

执行

```shell
python main.py
```

![执行](img/执行.png)

点击按钮

![点击按钮](img/点击按钮.png)
