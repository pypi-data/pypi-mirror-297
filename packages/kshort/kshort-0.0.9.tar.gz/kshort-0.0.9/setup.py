from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.9'
DESCRIPTION = 'Module to manage your projects using kitty and neovim'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="kshort",
    version=VERSION,
    author="McAlvaro",
    author_email="mc.alvaro641@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/McAlvaro/kshort',
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
