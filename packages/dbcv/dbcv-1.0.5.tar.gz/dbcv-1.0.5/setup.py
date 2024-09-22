from setuptools import setup, find_packages

setup(
    name='dbcv',
    version='1.0.5',
    author='db.boy',
    author_email='minkin.d.d@gmail.com',
    description='This library allows you to compute the Density-Based Clustering Validation metric quickly and with low memory consumption',
    long_description=open("README.md", 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/boyfws/DBCV',
    packages=find_packages(),
    install_requires=[
        'numba==0.60.0',
        'numpy>=1.19.5,<=1.26.4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'run_post_install=dbcv.setup_script:select_optimal_number_of_threads',
        ],
    },

)