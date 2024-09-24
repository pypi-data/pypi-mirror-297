from setuptools import setup, find_packages

setup(
    name='botnetv2',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'botnetv2=botnetv2:main',
        ],
    },
)
