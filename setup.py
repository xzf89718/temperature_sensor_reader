from setuptools import setup
from setuptools import find_packages


VERSION = '1.1.3'

setup(
    name='modbus_configuretools',  # package name
    version=VERSION,  # package version
    description="A package to read/write registers on a temperature sensor with python.",  # package description
    url="https://github.com/xzf89718/temperature_sensor_reader",
    packages=find_packages(),
    zip_safe=False,
    license="The MIT License",
    install_requires=["numpy", "pymodbus", "pyserial", "pyserial-asyncio"],
    author="XU Zifeng",
    author_email="zifeng.xu@foxmail.com"
)
