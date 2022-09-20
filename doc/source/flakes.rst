Nix Flakes
=============

Nix claims the reproducibility, but actually it is usually not the case:
- Nix can access arbitrary control files from different machines, for example,
    - ``~/.config/nixpkgs/config.nix``
    - Nix search path such as ``NIX_PATH``
    - Also, when we use `GitFetch` etc. to get the 3rd party libarary, it's difficult to absolutely make sure that the versions we get 
are the same from different builds.

Flakes are a solution to these problems. 

.. note::

    A flake is simply a source tree (such as a Git repository) containing a file named flake.nix, which provides a standardized interface to Nix packages (therefore, in most cases, the flake works with Git).


What is Nix Flake
***********

Flakes are self-contained units that have:

- inputs: dependencies
- outputs (packages, deployment instructions, Nix functions for use in other flakes). 

Flakes have great reproducibility because they are only allowed to depend on their inputs and they pin the exact versions of said inputs in a lockfile.


Create your first flake
***********
Here we provide an example about how to use ``flake`` to build ``netCDF``:

**Step 1: create an empty git repository**

First we need to create an empty git environment:

.. code-block:: bash

    git init netcdf-flake
    wget https://downloads.unidata.ucar.edu/netcdf-c/4.9.0/netcdf-c-4.9.0.tar.gz
    tar -zxvf netcdf-c-4.9.0.tar.gz
    git add netcdf-c-4.9.0

**Step 2: create flake.nix**

The command ``nix flake init`` creates a basic ``flake.nix`` for you. For example, we should go to the project root directory, and run

.. code-block:: bash

   nix flake init

Alternatively, we can create our own ``flake.nix``. An example is given below:

.. code-block:: bash

    {
        description = "A flake for building netCDF";

        inputs.nixpkgs.url = github:NixOS/nixpkgs/nixos-20.03;
        inputs.m4.url = "github:divnix/std";

        outputs = { self, nixpkgs }: {

            defaultPackage.x86_64-linux =
            # Notice the reference to nixpkgs here.
            with import nixpkgs { system = "x86_64-linux"; };
            stdenv.mkDerivation {
                name = "netcdf-flake";
                src = self;
                buildInputs = [ m4 zlib ];
                configurePhase = "cd netcdf-c-4.9.0; ./configure --disable-netcdf4 --disable-hdf5 --prefix /tmp/tmp/netcdf-flake";
                buildPhase = "make";
                installPhase = "make install; mkdir -p $out; mv /tmp/tmp/netcdf-flake/* $out";
            };

        };
    }

The above file can be explained as:

.. image:: sijin_nix5_env.PNG
   :width: 700px
   :height: 300px
   :scale: 100 %
   :alt: alternate text
   :align: left

An good example of the ``flake.nix`` can be found https://github.com/haskell/haskell-language-server/blob/master/flake.nix

Note that any file that is not tracked by Git is invisible during Nix evaluation, therefore we need to make ``flake.nix`` visible to Git:

.. code-block:: bash

    git add flake.nix

**Step 3: build the package**

There are a few methods to build the package:

- build the package automatically:

    - We can build the package automatically by running 
    
    .. code-block:: bash

        nix build
    
    within the directory where we have ``flake.nix``

- build the package step by step (e.g., debug):

    - For example, we can debug the different phases of the ``flake.nix`` file, if we want to debug `configurePhase`, we can do:

    .. code-block:: bash

        nix develop
        eval $configurePhase



Basic flake structure
***********

A Nix flake is a directory that contains a flake.nix file. That file must contain an attribute set with 

- one required attribute **outputs** and,
- optionally **description** and **inputs**.

Outputs
***********

**outputs** is a function that takes an attribute set of inputs:

    - **The most trival flake**: there is always at least one input: _self_, which refers to the flake that Nix is currently evaluating. 
    So, the most trivial flake possible is this:

        .. code-block:: bash

            {
                outputs = { self }: { };
            }

    This is a flake with no external inputs and no outputs (e.g., you can run it as ``nix build -f flake.nix``)


    - **The second flake**: we can add an arbitrary output to it

        .. code-block:: bash

            {
                outputs = { self }: {
                    foo = "bar";
                };
            }

    Here we added an output _foo_, which equals to ``bar``

    - **The 3rd flake**

        .. code-block:: bash

            {
                inputs = {
                    nixpkgs.url = "github:nixos/nixpkgs";
                };

                outputs = { self, nixpkgs }: {
                    packages.x86_64-linux.hello = nixpkgs.legacyPackages.x86_64-linux.hello;
                };
            }

    First of all, let's look at the properties

        - **packages.x86_64-linux.hello** here: this specify the target plaform (e.g., architecture + OS) which the package to be built on.
        In this case, we will build the package on ``x86_64-linux``

        - **nixpkgs.legacyPackages.x86_64-linux.hello**: nix will always try to install package (in this case ``hello``) from either of the following three channels:

            - hello
            - packages.x86_64-linux.hello
            - legacyPackages.x86_64-linux.hello

            where as we can see above, 
                - ``packages`` is used specifically for the Flakes; 
                - ``legacyPackages`` is designed specifically for nixpkgs (The nixpkgs repository 
                    is a lot older than flakes, so it is impossible to fit its arbitrary attribute format into neat packages).
                - if we directly try ``nix build hello`` it will try to search ``hello`` from the global flake registry (which we rarely use ...)

            In this case we will build the ``hello`` from the ``legacyPackages`` (or reexport ``hello`` from ``nixpkgs.legacyPackages.x86_64-linux`` in our own flake)
    
    - **A comprehensive example**
    

    
    