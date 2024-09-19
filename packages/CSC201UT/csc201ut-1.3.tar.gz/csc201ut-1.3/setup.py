"""
Python utilities used in CSC 201 at UT.
"""

import setuptools

# grab the README
with open("README.md", "r") as f:
    long_description = f.read()

# setup
setuptools.setup(
    name="CSC201UT",
    version="1.3",
    author="Dr. Jean Gourd",
    author_email="jgourd@ut.edu",
    description="Python utilities used in CSC 201 at UT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)

