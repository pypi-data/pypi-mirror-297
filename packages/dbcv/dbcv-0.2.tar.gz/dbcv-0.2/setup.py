from setuptools import setup, find_packages

from setuptools.command.install import install
from pathlib import Path
import subprocess
import sys

class CustomInstallCommand(install):
    def run(self):
        script_path = Path(__file__).parent / 'dbcv' / 'setup_script.py'
        subprocess.call([sys.executable, str(script_path)])
        install.run(self)

setup(
    name='dbcv',
    version='0.2',
    author='db.boy',
    author_email='minkin.d.d@gmail.com',
    description='This library allows you to compute the DBCV clustering metric quickly and with low memory consumption',
    long_description=open("README.md", 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/boyfws/DBCV',
    packages=find_packages(where='dbcv'),
    package_dir={'': 'dbcv'},
    install_requires=[
        'numba==0.60.0',
        'numpy>=1.19.5',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)