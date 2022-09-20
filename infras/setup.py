#!/usr/bin/env python

""" Setup for rainsat"""
from glob import glob

from setuptools import find_packages, setup


def main():
    return setup(
        author="A&M",
        author_email="zhans@transport.govt.nz",
        version="1.0",
        description="Shiny application",
        maintainer="A&M",
        maintainer_email="zhans@transport.govt.nz",
        name="shiny_app",
        packages=find_packages(),
        data_files=[
            ("base", glob("base/*")),
            ("../r", glob("r/*")),
        ],
        zip_safe=False,
    )


if __name__ == "__main__":
    main()
