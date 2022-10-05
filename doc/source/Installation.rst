Installation
=====

This page contains the instructions about how to install **SHINY_AWS**

Prerequisite
------
Tools like ``conda`` and ``cdk`` are required for installing **SHINY_AWS**. Please install them before the instruction or contact your Linux administor

conda Installation
^^^^^^^^^
**conda** is a package manager which support multiple languages including python. It can be installed as below:

- step 1: Download `miniconda` from  `[here] <https://docs.conda.io/en/latest/miniconda.html>`_
- step 2: the package can be installed as ``bash Miniconda3-latest-Linux-x86_64.sh``, or following the instruction `[here] <https://conda.io/projects/conda/en/latest/user-guide/install/linux.html>`_

After the installation, **conda** environment can be activated using ``conda activate <env>``


cdk Installation
^^^^^^^^^
The AWS CDK `[link] <https://docs.aws.amazon.com/cdk/v2/guide/home.html>`_ lets you build reliable, scalable, cost-effective applications in the cloud with the considerable expressive power of a programming language.

**CDK** can be installed as below:

- step 1: install ``PMN`` and ``Node`` (note that ``Node`` must have a version larger than `v12+`)
- step 2: install ``python`` (if you don't have one)
- step 3: then **cdk** can be easily installed as ``npm install -g aws-cdk``


SHINY_AWS Installation
^^^^^^^^^
After ``conda`` and ``cdk``, **SHINY_AWS** can be simply installed with the provided ``makefile`` in the repository:

.. code-block:: bash

   make all

The ``makefile`` file will call ``meta.yaml``, ``requirements.txt``, ``setup.py`` and ``env.yml``, and create a conda environment ``shiny_aws``, which contains all the dependancies.

The working environment then can be activated as ``conda activate shiny_aws``

.. note::

   The user may need to edit ``makefile`` and adapt the path of ``conda`` within it.