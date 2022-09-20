Basics
=====

This page records some useful basic concepts and commands for **nix** 

.. note::

   - **Nix store**: The approach taken by Nix is different. Nix stores all packages into a common place called the Nix store, usually located at `/nix/store`. Each package is stored in a unique subdirectory in the store, and each package has its own tree structure

Install nix
------
**nix** can be installed using the following command

.. code-block:: bash

   sh <(curl -L https://nixos.org/nix/install) --daemon

.. note::

   We may need to configure **nix** accordingly to use all of its features, e.g.,

   - | Set the environment variable ``XDG_CONFIG_HOME``, e.g.,
     |   ``export XDG_CONFIG_HOME=/home/szhang/.config``
   - | Edit ``$XDG_CONFIG_HOME/nix/nix.conf`` (we may need to create one if it does not exist) 
       and add the line ``experimental-features = nix-command flakes``.
     |   Note that by doing this we switch on the unstable version of **nix**,
         in order to keep using the stable version, we need to specify ``nixpkg`` in our future nix command, e.g., ``nix search nixpkgs emacs``
         instead of ``nix search emacs``


Use nix
------
.. list-table:: Packages
   :widths: 30 40 60
   :header-rows: 1

   * - Description
     - Command
     - Example
   * - Install a package
     - ``nix-env -i <pkg>`` or ``nix-env -iA <channel>.<pkg>``
     - ``nix-env -i hello`` or ``nix-env -iA nixpkgs.hello``
   * - Remove a package
     - ``nix-env -e <pkg>`` 
     - ``nix-env -e hello``
   * - Upgrade a package
     - ``nix-env --upgrade <pkg>`` 
     - ``nix-env --upgrade hello`` 
   * - Query installed packages
     - ``nix-env --query <pkg>`` 
     - ``nix-env --query hello`` or ``nix-env --query "*"``
   * - Search a package
     - ``nix search <channel> <pkg>`` 
     - ``nix search nixpkgs hello``
   * - Locate a package (within nix shell)
     - ``type <pkg>`` 
     - ``type hello``
   * - Search an excutable
     - ``command -v <pkg>``
     - N/A

.. list-table:: Channels (`all nix channels <https://channels.nixos.org/>`_)
   :widths: 30 40 60
   :header-rows: 1

   * - Description
     - Command
     - Example
   * - List existing channels
     - ``nix-channel --list`` 
     - N/A
   * - Add a new channel
     - - ``nix-channel --add <channel_link> <channel_name>``
       - `nix-channel --update`
     - - ``nix-channel --add https://nixos.org/channels/nixos-19.03 nixpkgs``
       - ``nix-channel --update``
   * - Remove a channel
     - - ``nix-channel --remove <channel_name>``
       - ``nix-channel --update`` 
     - - ``nix-channel --remove https://nixos.org/channels/nixos-19.03 nixpkgs``
       - ``nix-channel --update``


.. list-table:: Build (see Advanced for more details)
   :widths: 30 40 60
   :header-rows: 1

   * - Description
     - Command
     - Example
   * - build a package
     - ``nix-build '<channel name>' -A <pkg>``
     - ``nix-build '<nixpkgs>' -A <hello>``
   * - clean up nix store (unused packages)
     - ``nix-collect-garbage``
     - N/A

.. list-table:: Flakes
   :widths: 30 40 60
   :header-rows: 1

   * - Description
     - Command
     - Example
   * - show the outputs of a flake URL
     - ``nix flake show '<URL>'``
     - ``nix flake show nixpkgs``
   * - clone the flake source to a local directory
     - ``nix flake clone <URL> -f <local>``
     - ``nix flake clone git+https://github.com/balsoft/hello-flake/ -f hello-flake``

Reference
------
- https://rgoswami.me/posts/ccon-tut-nix/

- https://nix-tutorial.gitlabpages.inria.fr/nix-tutorial/getting-started.html

- https://www.tweag.io/blog/2020-05-25-flakes/

- https://serokell.io/blog/practical-nix-flakes