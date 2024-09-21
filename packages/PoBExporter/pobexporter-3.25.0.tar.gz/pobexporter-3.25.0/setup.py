import os
from setuptools import setup
import sys

# Package meta-data.
NAME = "PoBExporter"
DESCRIPTION = "Python library to generate Path of Building exports directly from PoE API without running PoB headless"
URL = "https://github.com/Liberatorist/PoBExporter"
EMAIL = ""
AUTHOR = "Liberatorist"
REQUIRES_PYTHON = ">=3.11.0"
VERSION = "3.25.0"

# What packages are required for this module to be executed?
REQUIRED = []

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}
data_files = []
for file in os.listdir("data"):
    # not packing all stat translations for now
    data_files.append(os.path.join("data", file))
directory = "/".join(sys.prefix.split("/")[:-2]) + "/data/data"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=["__init__"],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    license="proprietary",

    data_files=[
        (directory, data_files),
    ]

)
