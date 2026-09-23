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

Both tests run against the same dataset, ``WarpApofTutorial`` (5 apoferritin tilt series from
EMPIAR-10491) -- see :doc:`test_data` for how to download it, its expected folder layout, and
the acquisition parameters used when importing it.

Both ``apof_warp`` and ``apof_aretomo3`` resolve the dataset automatically at
``$ROOT/testdata/WarpApofTutorial`` (via ``TestData.get_dataset_path('WarpApofTutorial')``) --
no further configuration is needed. If the folder does not exist on disk, the tests fail
immediately with a message explaining how to download it.


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
