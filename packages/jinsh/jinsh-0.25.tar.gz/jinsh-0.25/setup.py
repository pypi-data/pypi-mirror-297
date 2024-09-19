###
# python setup.py sdist
# python setup.py sdist bdist_wheel
# easy_install xxx.tar.gz
# pip install -U example_package.whl
# ##

import PIL
from setuptools import setup, find_packages

setup(
    name='jinsh',# 自定义工具包的名字
    version='0.25',# 版本号
    author="Walter",  # 作者名字
    author_email="jinshuhaicc@gmail.com",  # 作者邮箱
    description="tool",  # 自定义工具包的简介
    license='MIT-0',  # 许可协议
    packages=find_packages(),
    install_requires=[
        "pillow",
        "oracledb",
        "json5",
        "oci",
        "urllib3",
        "gTTS",
        "SQLAlchemy",
        "PyMySQL",
        "mysql-connector-python",
        "pycryptodome",
        "openpyxl",
        "pandas",
        "opencv-python",
        "opencv-python-headless",
        "numpy",
        "matplotlib"
    ],
)


