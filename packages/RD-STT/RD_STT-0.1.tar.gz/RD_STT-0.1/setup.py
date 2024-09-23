from setuptools import setup,find_packages
setup(
    name='RD_STT',
    version='0.1',
    author='Ritik Dwivedi',
    author_email="example@gmail.com",
    description=" this is speech to text package created by Ritik Dwivedi",

)
packages=find_packages(),
install_requirements=[
    'selenium',
    'webdriver_manager',

]
