Installation
=====

This page contains the instructions about how to install **SHINY_AWS**

.. note::

   - Tools like ``conda`` (for BSIS) and ``cdk`` (for ASIS) are required for installing **SHINY_AWS**. Please install them before the instruction or contact your Linux administor.

Install BSIS
------
**BSIS** can be simply install with the provided ``makefile``

.. code-block:: bash

   make bsis

The make file will call ``meta.yaml``, ``setup.py`` and ``env.yml``, and create a conda environment in 