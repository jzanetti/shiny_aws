SHINY_AWS utilities
=====

**SHINY_AWS** utilities are provided to describe/update running shiny applications

The utilities are installed with all other **SHINY_AWS** components (such as **ASIS** or **BSIS**), and it can be simply called by

.. code-block:: bash

    app_utils
            --job <JOB NAME> 
            --name <SHINY APPLICATION NAME>


where:

- ``--job`` is the job type to be carried out. Currently we can choose it from:
    - ``showip``: showing the IP for the shiny application that can be accessed by the public
    - ``terminate``: terminating an shiny application
    - ``makeami``: making an AMI from an existing server (shiny application)

- ``--name`` is the shiny application name to be described/updated. It is usually the configuration filename for the shiny application.

For example, we can use the following command to shutdown a shiny application called ``test_shiny``

.. code-block:: bash

    app_utils --job terminate --name test_shiny