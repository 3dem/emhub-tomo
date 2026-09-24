Program Launchers
==================

In **emwrap**, external programs can be defined by specifying "program launchers". The idea of the launcher is to create a bash script that wraps the program call and sets up the necessary environment. For example, the launcher can load cluster modules, source bash files, or set up environment variables. In that way, the code from **emwrap** just needs to call the launcher without taking care of local installation details.

Jobs implemented in **emwrap** itself are launched via ``emh-tomo --launch MODULE`` (configured as the default ``EMWRAP`` launcher in *EMWRAP_CONFIG*, typically ``$ROOT/emh-tomo --launch``). Submitting jobs from the Relion GUI uses the ``relion_dispatcher`` entry in *EMWRAP_CONFIG* (typically ``$ROOT/emh-tomo --submit``).

There is a section in the *EMWRAP_CONFIG* variable related to the launchers:

.. code-block:: json

   "programs": {
        "EMWRAP": {"launcher": "$ROOT/emh-tomo --launch"},
        "WARP": {"launcher": "$SCRIPTS/warp_launcher.sh"},
        "PYTOM": {"launcher": "$SCRIPTS/pytom_launcher.sh"},
        "RELION": {"launcher": "$SCRIPTS/relion_launcher.sh"},
        "MOTIONCOR2": {"launcher": "$SCRIPTS/motioncor2.sh"},
        "MOTIONCOR3": {"launcher": "$SCRIPTS/motioncor3.sh"},
        "ARETOMO2": {"launcher": "$SCRIPTS/aretomo2.sh"},
        "ARETOMO3": {"launcher": "$SCRIPTS/aretomo3.sh"},
        "IMOD": {"launcher": "$SCRIPTS/imod_launcher.sh"},
        "CTFFIND": {"launcher": "$SCRIPTS/ctffind5.sh", "version": 5},
        "CRYOCARE": {"launcher": "$SCRIPTS/cryocare_launcher.sh"},
        "DENOISET": {"launcher": "$SCRIPTS/denoiset_launcher.sh"},
        "MISSALIGNMENT": {"launcher": "$SCRIPTS/missalignment.sh"}
    }

.. _supported-programs:

Supported Programs
------------------

The table below lists the external programs that **EMhub-Tomo** runs under the hood, the version
set in the launcher templates shipped with **emwrap** (``emwrap/config/scripts``), and where to find
installation instructions. These are the versions used for development and testing. Other
versions may work, but they have not been tested. Most programs are also available through
`SBGrid <https://sbgrid.org/>`_, which is how several of the example launchers load them.

.. list-table::
   :header-rows: 1
   :widths: 16 16 22 20 26

   * - Program
     - Config key
     - Launcher template
     - Tested version
     - Installation
   * - Warp / WarpTools / M
     - ``WARP``
     - ``warp_launcher.sh``
     - 2.0.0dev36
     - `Warp installation <https://warpem.github.io/warp/user_guide/warptools/installation/>`_
   * - RELION
     - ``RELION``
     - ``relion_launcher.sh``
     - 5.1.0-beta (CUDA 13.0)
     - `RELION installation <https://relion.readthedocs.io/en/release-5.0/Installation.html>`_
   * - pytom-match-pick
     - ``PYTOM``
     - ``pytom_launcher.sh``
     - 0.13.2
     - `pytom-match-pick docs <https://sbc-utrecht.github.io/pytom-match-pick/>`_
   * - AreTomo2
     - ``ARETOMO2``
     - ``aretomo2.sh``
     - 1.0.0
     - `AreTomo2 on GitHub <https://github.com/czimaginginstitute/AreTomo2>`_
   * - AreTomo3
     - ``ARETOMO3``
     - ``aretomo3.sh``
     - 2.2.8
     - `AreTomo3 on GitHub <https://github.com/czimaginginstitute/AreTomo3>`_
   * - IMOD
     - ``IMOD``
     - ``imod_launcher.sh``
     - 5.1.9
     - `IMOD download <https://bio3d.colorado.edu/imod/download.html>`_
   * - DenoisET
     - ``DENOISET``
     - ``denoiset.sh``
     - conda env ``denoiset``
     - `DenoisET on GitHub <https://github.com/apeck12/denoiset>`_
   * - MissAlignment
     - ``MISSALIGNMENT``
     - ``missalignment.sh``
     - conda env ``miss-alignment``
     - `MissAlignment on GitHub <https://github.com/warpem/miss-alignment>`_

.. note::

   The Warp tilt-series alignment job (``emw-warp-tsalign``) also calls AreTomo2/AreTomo3 or IMOD,
   depending on the alignment method selected, so those launchers must work for the Warp pipeline too.

After the installation, there is a *scripts* folder that is created with some of the launcher scripts, but YOU MIGHT NEED TO MODIFY them to work in your environment. In the following sections, there are some examples of launchers.

Warp Launcher
-------------

In the following example, Warp is loaded from the available modules, together with Aretomo2, version 1.0.0.

.. code-block:: bash

   #!/bin/bash

   PROGRAM=$1
   shift

   export MODULES="warp/2.0dev33-latest aretomo2/1.0.0"
   echo Loading modules $MODULES
   module load -s $MODULES

   $PROGRAM $@

Or, if we are loading Warp from an SBGrid installation, the launcher could be something like:

.. code-block:: bash

   #!/bin/bash

   PROGRAM=$1
   shift

   export SBGRID=/programs/sbgrid.shrc
   source $SBGRID
   echo "Loading Warp from SBGrid file: ${SBGRID}."

   $PROGRAM $@

Relion Launcher
----------------

In the case of the Relion launcher, the first argument is the program name, and the second is the number of MPI processes. The wrapper will take care of adding the *_mpi* suffix to the program and also the *mpirun* command. For example:

.. code-block:: bash

    #!/bin/bash

    export SBGRID=/programs/sbgrid.shrc
    source $SBGRID
    echo "Loading Relion from SBGrid file: ${SBGRID}."

    export PROGRAM=$1
    shift
    export MPI=$1
    shift

    if [ "$MPI" -eq 1 ]; then
        export CMD="${PROGRAM} $@"
    else
        export CMD="mpirun.relion --oversubscribe -np ${MPI} ${PROGRAM}_mpi $@"
    fi

    echo Running command: ${CMD}
    $CMD

Other Launchers
----------------

**emwrap** is still under development, and more tools will be integrated in the future. Right now, apart from Warp and Relion, it might be helpful to configure the following launchers:

* PyTOM launcher: for 3D template matching
* IMOD launcher: for etomo tilt-series alignment
