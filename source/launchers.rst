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
        "IMOD": {"launcher": "$SCRIPTS/imod_launcher.sh"},
        "MOTIONCOR2": {"launcher": "$SCRIPTS/motioncor2.sh"},
        "MOTIONCOR3": {"launcher": "$SCRIPTS/motioncor3.sh"},
        "ARETOMO2": {"launcher": "$SCRIPTS/aretomo2.sh"},
        "ARETOMO3": {"launcher": "$SCRIPTS/aretomo3.sh"},
        "CTFFIND": {"launcher": "$SCRIPTS/ctffind5.sh", "version": 5},
        "CRYOCARE": {"launcher": "$SCRIPTS/cryocare_launcher.sh"}
    }

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
