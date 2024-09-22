from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyside_socket_async",
    version="0.1.8",
    author="chakcy",
    author_email="947105045@qq.com",
    description="PySide6 Socket Async",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/cai-xinpenge/pyside_socket_async",
    include_package_data=True,
    packages=(
        find_packages(where=".")
    ),
    package_dir={
        "": ".",
        "pyside_socket_async":"./pyside_socket_async"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12.4',
    install_requires=[   
        "pydantic>=2.9.1",
        "PySide6>=6.7.2",
        "requests>=2.32.3",
        "colorlog>=6.8.2"
    ]
)