from setuptools import setup, find_packages

setup(
    name='socket-sdk',
    version='0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-socketio[client]',
        'dataclasses-json'
    ],
    author='',
    author_email='',
    description='',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)