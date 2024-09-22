from setuptools.command.build_py import build_py
from setuptools.command.install import install
import subprocess
import sys
from pathlib import Path
from setuptools import setup, find_packages


class CustomBuildCommand(build_py):
    """Custom handler for the 'build_py' command."""
    
    def run(self):
        super(build_py, self).run()
        script_path = Path(__file__).parent / 'setup_script.py'
        subprocess.call([sys.executable, str(script_path)])


class CustomInstallCommand(install):
    
    def run(self):
        super(install, self).run()
        script_path = Path(__file__).parent / 'setup_script.py'
        subprocess.call([sys.executable, str(script_path)])

setup(
    name='dbcv',
    version='0.0.2',
    author='db.boy',
    author_email='minkin.d.d@gmail.com',
    description='This library allows you to compute the DBCV clustering metric quickly and with low memory consumption',
    long_description=open("README.md", 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/boyfws/DBCV',
    packages=find_packages(),
    install_requires=[
        'numba==0.60.0',
        'numpy>=1.19.5,<=1.26.4',
    ],
    cmdclass={
        'build_py': CustomBuildCommand,  
        'install': CustomInstallCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    include_package_data=True,
)