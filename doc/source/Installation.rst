Installation
=====

This page contains the instructions about how to install **SHINY_AWS**

The package management tool ``conda`` is required for installing **SHINY_AWS**. Please install it before the instruction or contact your Linux administor

CONDA Installation
^^^^^^^^^
**CONDA** is a package manager which support multiple languages including python. It can be installed as below:

- **step 1**: Download `miniconda` from  `[here] <https://docs.conda.io/en/latest/miniconda.html>`_
- **step 2**: the package can be installed as ``bash Miniconda3-latest-Linux-x86_64.sh``, or following the instruction `[here] <https://conda.io/projects/conda/en/latest/user-guide/install/linux.html>`_

After the installation, **CONDA** environment can be activated using ``conda activate <env>``


SHINY_AWS Installation
^^^^^^^^^
After ``conda``, **SHINY_AWS** can be simply installed with the provided ``makefile`` in the repository:

.. code-block:: bash

   export CONDA_BASE=<CONDA PATH>
   export PLATFORM=<PLATFORM TYPE>
   sudo -E make all

where ``CONDA_BASE`` is the path where the ``conda`` package is installed. For example, we can have ``export CONDA_BASE=~/Programs/miniconda3/``.
``PLATFORM`` indicates which platform to be used, we should set it to either ``mac`` or ``linux``. 

The ``makefile`` file collects information from ``meta.yaml``, ``requirements.txt``, ``setup.py`` and ``env.yml``, and creates a conda environment ``shiny_aws``, which contains all the dependancies.

The working environment then can be activated as:

.. code-block:: bash

   conda activate shiny_aws