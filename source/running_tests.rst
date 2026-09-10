Running Tests
==============

**emwrap** ships integration tests that run a small real processing pipeline end-to-end (import, alignment, CTF, reconstruction, and optionally particle extraction/refinement) against a shared tilt-series dataset, and check that every job in the pipeline finishes successfully and produces the expected output files.

Tests are exposed as subcommands of the ``./emh-tomo`` entry point, through the ``--test`` action:

.. code-block:: bash

   # List the available tests
   ./emh-tomo --test list

   # Show the options for a specific test
   ./emh-tomo --test apof_warp -h
   ./emh-tomo --test apof_aretomo3 -h

   # Run a test
   ./emh-tomo --test apof_warp
   ./emh-tomo --test apof_aretomo3


Test Data
---------

Both tests run against the same tilt-series dataset: the 5 apoferritin (ApoF) tilt series from `EMPIAR-10491 <https://www.ebi.ac.uk/empiar/EMPIAR-10491/>`_, which is also the dataset used by Warp's own `WarpTools tilt series quick start guide <https://warpem.github.io/user_guide/warptools/quick_start_warptools_tilt_series/>`_.

Downloading the dataset
........................

Datasets are no longer configured through ``EMWRAP_CONFIG``. Each named dataset is now expected under ``$ROOT/testdata/<NAME>/`` (``ROOT`` is the installation folder, i.e. the directory containing ``emwrap.bashrc``), and **emwrap** can download the known datasets there for you, using the ``data`` action of the same ``./emh-tomo --test`` entry point used to run the tests:

.. code-block:: bash

   # List available datasets
   ./emh-tomo --test data --list

   # Download to $ROOT/testdata/WarpApofTutorial/
   ./emh-tomo --test data --download WarpApofTutorial

   # Or download to a custom location (PATH/WarpApofTutorial)
   ./emh-tomo --test data --download WarpApofTutorial /path/to/testdata

``--list`` currently reports two known datasets, ``WarpApofTutorial`` (`EMPIAR-10491 <https://www.ebi.ac.uk/empiar/EMPIAR-10491/>`_, used by both ``apof_warp`` and ``apof_aretomo3``) and ``RelionTomoTutorial`` (`EMPIAR-10164 <https://www.ebi.ac.uk/empiar/EMPIAR-10164/>`_, not yet used by any test) -- the rest of this section only concerns ``WarpApofTutorial``.

Once downloaded, ``$ROOT/testdata/WarpApofTutorial/`` should look like this:

.. code-block:: text

   testdata/WarpApofTutorial/
   ├── gain_ref.mrc
   ├── mdoc/
   │   ├── TS_1.mrc.mdoc
   │   ├── TS_11.mrc.mdoc
   │   └── ...
   └── frames/
       ├── 2Dvs3D_53-1_00001_...tif
       └── ...

This layout matches what the test workflows expect for the ``emw-import-ts`` job (``data/gain_ref.mrc``, ``data/mdoc/*.mdoc``, ``data/frames/``), and reflects the dataset's own acquisition parameters used by the test workflows: a pixel size of 0.789 Å, 300 kV, Cs 2.7 mm, a per-tilt dose of 2.64 e⁻/Å², and a tilt-axis angle of -85.6°.

Both ``apof_warp`` and ``apof_aretomo3`` resolve the dataset automatically at ``$ROOT/testdata/WarpApofTutorial`` (via ``TestData.get_dataset_path('WarpApofTutorial')``) -- no further configuration is needed. If the folder does not exist on disk, the tests fail immediately with a message explaining how to download the data.


Common Options
---------------

Both tests share the same base set of options (defined in the shared ``TestApoF`` test case):

.. list-table::
   :header-rows: 1
   :widths: 20 60 20
   :width: 100%

   * - Option
     - Description
     - Default
   * - ``--project``, ``-p PATH``
     - Project folder where the test pipeline is run. When omitted, a temporary folder is created and removed automatically at the end of the test; passing a path keeps the outputs around for inspection.
     - temporary folder
   * - ``--ts NAME``
     - Restrict the run to a single tilt series (e.g. ``TS_11``) instead of all of them.
     - ``*`` (all)
   * - ``--gpus``, ``-g N``
     - Number of GPUs to request for GPU-enabled jobs.
     - ``1``
   * - ``--dry``
     - Dry run: load and validate the workflow and print which jobs would run, without actually launching them.
     - off
   * - ``-v``, ``--verbose``
     - Increase the verbosity of the underlying ``unittest`` output. Can be repeated (``-vv``).
     - off


Available Tests
-----------------

apof_warp
..........

Runs the Warp-based ApoF preprocessing pipeline (``TestApoFWarp``). It adds one extra option on top of the common ones:

.. list-table::
   :header-rows: 1
   :widths: 20 60 20
   :width: 100%

   * - Option
     - Description
     - Default
   * - ``--workflow``, ``-w {small,medium,full,otf}``
     - Selects how much of the pipeline to run (see below).
     - ``small``

The ``--workflow`` choices run progressively more of the pipeline:

* ``small`` -- preprocessing only: ``emw-import-ts``, ``emw-warp-mctf`` (motion correction and CTF), ``emw-warp-tsalign`` (tilt-series alignment), and ``emw-warp-ctfrec`` (3D CTF and reconstruction).
* ``medium`` -- the ``small`` jobs plus particle picking and an initial 3D refinement: ``emw-pytom``, ``emw-warp-export_particles``, and ``relion.initialmodel.tomo``.
* ``full`` -- intended to also run 3D refinement after the initial model; **work in progress**, not implemented yet.
* ``otf`` -- runs preprocessing in on-the-fly (OTF) mode instead, using a single combined ``emw-warp-otf`` job (import + alignment + reconstruction) rather than the separate ``small``-style steps.

Examples:

.. code-block:: bash

   # Run the default (small) workflow with a temporary project folder
   ./emh-tomo --test apof_warp

   # Run the medium workflow, keeping outputs, using 2 GPUs
   ./emh-tomo --test apof_warp --workflow medium --project /tmp/apof_warp_run --gpus 2

   # Only check that the workflow and test data are set up correctly
   ./emh-tomo --test apof_warp --dry


apof_aretomo3
..............

Runs the AreTomo3-based ApoF preprocessing pipeline (``TestAretomo3ApoF``): ``emw-import-ts`` followed by ``emw-aretomo3``, which performs tilt-series alignment and reconstruction in a single job. It does not add any options beyond the `Common Options`_.

.. code-block:: bash

   # Run with a temporary project folder
   ./emh-tomo --test apof_aretomo3

   # Run a single tilt series, keeping outputs, with verbose unittest output
   ./emh-tomo --test apof_aretomo3 --ts TS_11 --project /tmp/apof_aretomo3_run -v
