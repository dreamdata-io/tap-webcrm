#!/usr/bin/env python

from setuptools import setup

setup(
    name="tap-webcrm",
    version="0.0.1",
    description="Singer.io tap for extracting data AgileCMS",
    author="Dreamdata",
    url="https://dreamdata.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    install_requires=["singer-python==5.8.1", "requests", "cachetools==3.1.1"],
    entry_points="""
        [console_scripts]
        tap-webcrm=tap_webcrm:main
    """,
    include_package_data=True,
    package_data={
        "tap_webcrm": [
            "swagger/swagger.json",
            "schemas/opportunity.json",
            "schemas/organisation.json",
            "schemas/person.json",
        ]
    },
    packages=["tap_webcrm"],
    setup_requires=["pytest-runner"],
    extras_require={"test": [["pytest"]]},
)
