"""
requires  pip install setuptools wheel
"""

from setuptools import setup, find_packages

setup(
    name="pysell",
    version="1.2.5",
    description="A Python-based Simple E-Learning Language for the Rapid Creation of Interactive and Mobile-Friendly STEM Courses",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andreas Schwenk",
    author_email="contact@compiler-construction.com",
    url="https://pysell.org",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "pysell=pysell.sell:main",
        ],
    },
    include_package_data=True,
    license="GPL-3.0-or-later",
    keywords="dsl quiz learning stem teaching assessment",
)
