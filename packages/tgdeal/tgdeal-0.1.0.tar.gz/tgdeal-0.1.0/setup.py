from setuptools import find_packages, setup
import subprocess
import pkg_resources
import sys


def check_and_install(package, spec_name=None):
    try:
        pkg_resources.require(package)
        print(f"{package} is already installed.")

    except pkg_resources.DistributionNotFound:
        subprocess.check_call([sys.executable, "-m", "pip", "install", spec_name or package])


setup(
    name='tgdeal',
    packages=find_packages(exclude=['tests']),
    version='0.1.0',
    description='B2B API client of the telegram buying service',
    author='TeleDealer',
    license='MIT',
    install_requires=[
        'simple_singleton',
        'pydantic',
        'httpx'
    ]
)
