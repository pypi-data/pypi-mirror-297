# setup.py
from setuptools import setup, find_packages

setup(
    name='my_framework_3',
    version='0.1',
    description='A simple Python framework',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'my_framework_3=my_framework_3.main:greet',  # Allows running with the command `my_framework`
        ],
    },
)

