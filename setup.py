#!/usr/bin/env python
import os
from setuptools import setup

version = os.environ.get("PACKAGE_VERSION") or os.environ.get("CIRCLE_TAG")
url = "https://github.com/dreamdata-io/tap-webcrm"


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tap-webcrm",
    version=version,
    description="Singer.io tap for extracting data from WebCRM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dreamdata",
    url=url,
    download_url=f"{url}/archive/v{version}.tar.gz",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    license="MIT",
    install_requires=[
        "singer-python>=5.8, <6",
        "requests>=2.22.0",
        "cachetools>=3.1.1",
    ],
    entry_points="""
        [console_scripts]
        tap-webcrm=tap_webcrm:main
    """,
    include_package_data=True,
    package_data={"tap_webcrm": ["swagger/*", "schemas/*",]},
    keywords=["singer", "io", "webcrm", "etl", "crm"],
    packages=["tap_webcrm"],
    setup_requires=["pytest-runner"],
    extras_require={"test": [["pytest"]]},
)
