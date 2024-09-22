from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Module to manage your projects using kitty and neovim'

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name="kshort",
    version=VERSION,
    author="McAlvaro",
    author_email="mc.alvaro641@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    url='',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'kshort'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'kshort=kshort.main:main'
        ]
    }
)
