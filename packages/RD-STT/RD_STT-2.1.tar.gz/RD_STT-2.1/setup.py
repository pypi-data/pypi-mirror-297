from setuptools import setup, find_packages

setup(
    name='RD_STT',
    version='2.1',
    author='Ritik Dwivedi',
    author_email="example@gmail.com",
    description="This is a speech-to-text package created by Ritik Dwivedi",
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver_manager',
    ],
)
