from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mab_algo',
    version='1.0.0',
    url='https://github.com/LavishKK2022/mab_algo',
    author='Lavish Kamal Kumar',
    author_email='dev@lavish-kumar.com',
    description='Implementation of Multi Armed Bandit algorithms from "Reinforcement Learning - An Introduction" by Richard S. Sutton and Andrew G. Barto',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)
