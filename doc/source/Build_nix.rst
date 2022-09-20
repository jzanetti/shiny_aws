Build my first package
=====

In the section, we create a nix derivation for installing netCDF package


Create the derivation script
*************

First we need to create the ``default.nix`` as below:

.. code-block:: bash

      { 
      # pkgs ? import (fetchTarball https://channels.nixos.org/nixpkgs-22.05-darwin/nixexprs.tar.xz) {} # use default
      pkgs ? import <nixpkgs> {} # use default
      }:

      with pkgs; 

      let
         packages = rec {
            nc = pkgs.stdenv.mkDerivation rec {
                  pname = "netcdf-c";
                  version = "3.9-test";

                  src = pkgs.fetchurl {
                     url = "https://downloads.unidata.ucar.edu/netcdf-c/4.9.0/netcdf-c-4.9.0.tar.gz";
                     sha256 = "sha256-TJVgIrecCOXhTu6N9RsTwo5hIcK35/qtwhs3WUlAC0k=";
                  };

                  buildInputs = [
                     pkgs.cmake
                     pkgs.gcc
                     pkgs.m4
                     pkgs.zlib
                  ];

                  configurePhase = ''
                     ./configure --disable-netcdf4 --disable-hdf5 --prefix /tmp/tmp/netcdf-install
                  '';

                  buildPhase = ''
                     make
                  '';

                  installPhase = ''
                     make install
                     mkdir -p $out
                     mv /tmp/tmp/netcdf-install/* $out
                  '';
                  shellHook = ''
                     LD_LIBRARY_PATH=$out/lib:$LD_LIBRARY_PATH
                     PATH=$out/bin:$PATH
                  '';
         };
         # The shell of our experiment runtime environment
            expEnv = mkShell rec {
               name = "exp01Env";
               buildInputs = [nc];
            };
         };
      in 
         packages 

This file looks similar to the one discussed in previous section, but its structure changed a little. The main difference is that:

the file does not return a single derivation (the chord package) but a set with several attributes:

- nc: where the actual package to be installed
- expEnv: shell environment to be used to run the experiment

.. note::

    the structure for the ``.nix`` is:
    
    .. code-block:: bash

        {pkgs ? import ....}:

        with pkgs;
          let
              packages = rec {
              
                  pkg1 = pkgs.stdenv.mkDerivation rec { ... };
                  pkg2 = ....
                  ....
                  env1 = mkShell rec { ... };
                  env2 = ...
                  ....
              };
        in 
          packages 


Build the package
*************

We can use both ``nix-shell`` or ``nix-build`` for the above file, while we need to tell the command on which attribute to be used (e.g., whether it is ``nc`` or ``expEnv``)

.. code-block:: bash

   nix-build default.nix -A nc

We will see all the binaries and libraries are built in ./result, which is linked to the nix store (e.g., ``/nix/store/xxlf2ndmajaadbcrlgj0nfcj023vhg5a-netcdf-c-3.9-test``).

Run the package
*************

**Option 1: run the package manually within the shell**

After the build (last step), we can run ``netCDF`` within the environment of ``expEnv``

.. code-block:: bash

   nix-shell default2.nix -A expEnv

After this we can test ``ncdump`` within the nix shell (e.g., ``ncdump --help``)

**Option 2: run the package with command**

We can define a script (e.g., for using ``ncdump``) so we don't have to manually get into the nix shell. For example, the script (e.g., ``test.sh``) can be something like

.. code-block:: bash

    #!/usr/bin/env bash
    ncdump --help

Then we can execute ``test.sh`` within the nix-shell as:

.. code-block:: bash

    nix-shell default.nix -A expEnv --command ./test.sh

**Option 3: define the command with the derivation script**

We can define the runtime script within the nix derivation shell, so everytime we don't even  need to attach ``--command``. 
In order to do so, we need to add ``shellHook`` under ``mkShell rec``. For example,

.. code-block:: bash

    expEnv = mkShell rec {
        name = "exp01Env";
        buildInputs = [nc];
        shellHook = "./test.sh";
    };

Then we can execute ``test.sh`` simply by

.. code-block:: bash

    nix-shell default.nix -A expEnv

  
**Option 4: nix-shell shebang**

We even don't have to call ``nix-shell`` even we need to use ``nix`` package or environment. In order to do so, we can use ``shebang``.
For example, we can have a shebang script (e.g., ``test_shebang.sh``) as:

.. code-block:: bash

    #!/usr/bin/env nix-shell
    #!nix-shell default3.nix -A expEnv -i bash
    ncdump --help
  
Then we can execute the ``test_shebang.sh`` as;

.. code-block:: bash

    ./test_shebang.sh

    