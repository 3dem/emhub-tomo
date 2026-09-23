Test Data
==========

**emwrap** ships small, real tilt-series datasets used by its automated tests and by the
tutorials in this documentation. Datasets are no longer configured through
``EMWRAP_CONFIG``: each named dataset is expected under ``$ROOT/testdata/<NAME>/`` (``ROOT``
is the installation folder, i.e. the directory containing ``emwrap.bashrc``), and **emwrap**
can download the known datasets there for you.

Downloading a Dataset
-----------------------

Datasets are downloaded with the ``data`` action of the same ``./emh-tomo --test`` entry point
used to run the tests (see :doc:`running_tests`):

.. code-block:: bash

   # List available datasets
   ./emh-tomo --test data --list

   # Download to $ROOT/testdata/<NAME>/
   ./emh-tomo --test data --download <NAME>

   # Or download to a custom location (PATH/<NAME>)
   ./emh-tomo --test data --download <NAME> /path/to/testdata

If a dataset's folder does not exist on disk when a test or job that needs it runs, it fails
immediately with a message explaining how to download it.

Available Datasets
---------------------

``--list`` currently reports two known datasets:

.. list-table::
   :header-rows: 1
   :widths: 22 18 25 35
   :width: 100%

   * - Name
     - Source
     - Tilt Series
     - Used by
   * - ``WarpApofTutorial``
     - `EMPIAR-10491 <https://www.ebi.ac.uk/empiar/EMPIAR-10491/>`_,
       `EMD-15854 <https://www.ebi.ac.uk/emdb/EMD-15854>`_
     - TS_1, TS_11, TS_17, TS_23, TS_32
     - ``apof_warp``, ``apof_aretomo3``, :doc:`warp_apof_tutorial`
   * - ``RelionTomoTutorial``
     - `EMPIAR-10164 <https://www.ebi.ac.uk/empiar/EMPIAR-10164/>`_
     - TS_01, TS_03, TS_43, TS_45, TS_54
     - *(not yet used by any test or tutorial)*

WarpApofTutorial
~~~~~~~~~~~~~~~~~~

5 apoferritin (ApoF) tilt series from `EMPIAR-10491 <https://www.ebi.ac.uk/empiar/EMPIAR-10491/>`_,
the same dataset used by Warp's own
`WarpTools tilt series quick start guide <https://warpem.github.io/user_guide/warptools/quick_start_warptools_tilt_series/>`_.
This is the dataset used by the ``apof_warp`` and ``apof_aretomo3`` automated tests (see
:doc:`running_tests`), and by the :doc:`warp_apof_tutorial` walkthrough.

.. code-block:: bash

   ./emh-tomo --test data --download WarpApofTutorial

Once downloaded, ``$ROOT/testdata/WarpApofTutorial/`` should look like this:

.. code-block:: text

   testdata/WarpApofTutorial/
   ├── gain_ref.mrc
   ├── emd_15854.map
   ├── mdoc/
   │   ├── TS_1.mrc.mdoc
   │   ├── TS_11.mrc.mdoc
   │   └── ...
   └── frames/
       ├── 2Dvs3D_53-1_00001_...tif
       └── ...

This layout matches what the ``emw-import-ts`` job expects (``gain_ref.mrc``, ``mdoc/*.mdoc``,
``frames/``), and reflects the dataset's own acquisition parameters, used when importing the
tilt series: a pixel size of 0.789 Å, 300 kV, Cs 2.7 mm, a per-tilt dose of 2.64 e⁻/Å², and a
tilt-axis angle of -85.6°.

``emd_15854.map`` is the apoferritin reference map from
`EMD-15854 <https://www.ebi.ac.uk/emdb/EMD-15854>`_ (384³ voxels at 0.729 Å/px). It is not part
of EMPIAR-10491: it is downloaded separately from EMDB and used by the
``emw-pytom-create_template`` job to build the template and mask for template matching. EMDB
serves its maps gzipped, so it is decompressed after downloading (23 MB compressed, 216 MB on
disk).

.. TODO(screenshot): the downloaded WarpApofTutorial folder, or the project's Data tab
   pointing at it.

RelionTomoTutorial
~~~~~~~~~~~~~~~~~~~~

5 tilt series (TS_01, TS_03, TS_43, TS_45, TS_54) from
`EMPIAR-10164 <https://www.ebi.ac.uk/empiar/EMPIAR-10164/>`_, the dataset used by Relion's own
subtomogram averaging tutorial. Not yet used by any automated test or tutorial in this
documentation.

.. code-block:: bash

   ./emh-tomo --test data --download RelionTomoTutorial
