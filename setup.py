from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='digitalab',    # 包名
      version='0.1.0',        # 版本号
      description='',
      long_description=long_description,
      author='daijie',
      author_email='koryako@163.com',
      url='',
      install_requires=[],	# 依赖包会同时被安装
      license='MIT',
      packages=find_packages())

