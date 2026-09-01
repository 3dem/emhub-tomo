Python Environment
====================

EMhub-Tomo needs Python 3.8 or newer, made available through either a conda environment or a plain Python venv. The install script auto-detects whichever one is active when you run it and generates a `bashrc` file that (re)activates the same environment on every later run -- see `Re-activating the Environment`_ below.

Installing Conda
------------------

If you do not already have conda available, you can install Miniconda with:

.. code-block:: bash

   mkdir miniconda3 && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && bash ./miniconda.sh -b -u -p ./miniconda3

   # Make conda available in your current shell (only needed once per shell,
   # or add this line to your shell's startup file, e.g. ~/.bashrc)
   source miniconda3/etc/profile.d/conda.sh

Once conda is available, create and activate the environment used for the installation:

.. code-block:: bash

   conda create -y --name=emhub-tomo python=3.8 && conda activate emhub-tomo

Using Python 3.8 + venv Instead
---------------------------------

If you would rather not use conda, EMhub-Tomo also works with a plain Python venv:

.. code-block:: bash

   python3.8 -m venv venv && source venv/bin/activate

A few caveats with this path:

* Unlike conda, `venv` does not install a Python interpreter for you -- the exact `python3.8` (or whichever Python >= 3.8 you point it at) must already be installed on the system beforehand.
* You are responsible for installing that Python version yourself first (through your OS package manager, `pyenv`, building from source, etc.); `python3.8 -m venv ...` will fail if it is not already present.
* Make sure the venv is activated before running the installer, and remember it needs to be (re)activated the same way in any new shell where you run `emh-tomo` directly instead of through the generated `bashrc`.

Re-activating the Environment
--------------------------------

While running the installation, the install script tries to determine the conda path and the currently activated environment (conda or venv). Based on that, it creates a `bashrc` file in the installation folder that reactivates the same environment and exports `EMSTACK_HOME`; this file is what gets sourced from `emwrap.bashrc` every time `emh-tomo` runs.

If you are not using conda, or the generated `bashrc` file is not correct for your setup, edit it directly so that it properly loads the Python environment for launching **emhub/emwrap**:

.. code-block:: bash

   # Edit the bashrc file
   vim bashrc
