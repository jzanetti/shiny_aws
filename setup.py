#!/usr/bin/env python

""" Setup for shiny_aws"""
from glob import glob

from setuptools import find_packages, setup


def main():
    return setup(
        author="Sijin Zhang",
        author_email="zsjzyhzp@gmail.com",
        version="0.0.1",
        description="Shiny application infras (BSIS)",
        maintainer="Sijin",
        maintainer_email="zsjzyhzp@gmail.com",
        name="shiny_aws",
        packages=find_packages(),
        data_files=[
            ("etc/cfg", glob("etc/cfg/*")),
            ("etc/examples/hello_world", glob("etc/examples/hello_world/*")),
        ],
        zip_safe=False,
    )


if __name__ == "__main__":
    main()
