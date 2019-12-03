#!/usr/bin/env python

from setuptools import setup

version = "0.0.1"
url = "https://github.com/dreamdata-io/tap-webcrm"

setup(
    name="tap-webcrm",
    version=version,
    description="Singer.io tap for extracting data from WebCRM",
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
