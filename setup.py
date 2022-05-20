# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import os
from setuptools import find_packages, setup


def readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:

        long_description = f.read()
    return long_description


REQUIRED = [
    "certifi>=2020.4.5.1",
    "charset-normalizer>=2.0.0",
    "idna>=3.0",
    "numpy>=1.18.0",
    "pandas>=1.0.5",
    "Pillow>=8.0.0",
    "python-dateutil>=2.8.0",
    "pytz>=2020.1",
    "requests>=2.23.0",
    "setuptools>=59.1.0",
    "six>=1.14.0",
    "typing_extensions>=4.0.0",
    "urllib3>=1.26.2",
    "wheel>=0.36.0",
    "pip>=19.2.3"
]


# Package meta-data.
NAME = "digitalBrain"
DESCRIPTION = "sdk"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "1.3.rc"

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    license="MIT Licence",
    url="https://digital_brain.com",
    description=DESCRIPTION,
    # long_description=long_description,
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires=REQUIRES_PYTHON,
    # py_modules=['digitalBrain'],
    scripts=['./digitalBrain/api.py'],
    # if your src is a single module, use py_modules instead of 'packages':
    # packages=find_packages(),
    packages=find_packages(
        include=['digitalBrain']
    ),
    include_package_data=True,
    # entry_points={
    #     # 'console_scripts': ['mycli=src:detect_torch'],
    #     'setuptools.installation': ['mycli=digitalBrain:detect_torch'],
    # },
    install_requires=REQUIRED,
    # Trove classifiers
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
