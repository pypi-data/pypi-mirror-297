from setuptools import setup, find_packages
import os

from how2validate.utility.config_utility import get_version

# Retrieve the current version from environment variable
version = get_version()

# Get the path to requirements.txt which is one folder up
requirements_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'requirements.txt'))

# Read requirements from requirements.txt
with open(requirements_path, 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='how2validate',
    version=version,
    description='A cli and package for validating secrets.',
    author='VigneshKna',
    author_email='vigneshkna@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.txt', '../requirements.txt','.env',"./how2validate"],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'how2validate=how2validate.validator:main',
        ],
    },
)
