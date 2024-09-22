from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Module to manage your projects using kitty and neovim'

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

with open('requirements.txt', 'r') as requirements_file:
    install_requires = requirements_file.read()

setup(
    name="kshort",
    version=VERSION,
    author="McAlvaro",
    author_email="mc.alvaro641@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    packages=find_packages(),
    install_requires=install_requires,
    keywords=['python', 'kshort'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
