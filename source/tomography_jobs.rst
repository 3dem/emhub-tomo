Tomography Jobs
==================

The job types currently implemented in **emwrap** for CryoET processing, grouped by the external package they wrap. This list is generated from ``ProcessingConfig.get_jobs()`` and ``ProcessingConfig.get_packages()`` (in ``emwrap/base/config.py``); every job listed here ships with a matching form under ``emwrap/config/forms`` -- see :doc:`index` (Jobs and Workflows section) for how those forms are structured.

.. _Warp: https://warpem.github.io/
.. _Relion: https://relion.readthedocs.io/en/latest/STA_tutorial/Introduction.html
.. _PyTOM: https://github.com/SBC-Utrecht/pytom-match-pick
.. _AreTomo: https://github.com/czimaginginstitute/AreTomo3

emwrap
-------

General-purpose jobs that are not specific to any external package.

.. list-table::
   :header-rows: 1
   :widths: 30 40 20
   :width: 100%

   * - Job
     - Label
     - Output
   * - ``emw-import-ts``
     - EMwrap Import TS
     - EMwrap
   * - ``emw-subset-ts``
     - EMwrap Subset TS
     - EMwrap
   * - ``emw-merge-sets``
     - EMwrap Merge Sets
     - EMwrap
   * - ``emw-missalignment``
     - MissAlignment
     - MissAlignment

Warp
-----

Jobs wrapping `Warp`_.

.. list-table::
   :header-rows: 1
   :widths: 30 40 20
   :width: 100%

   * - Job
     - Label
     - Output
   * - ``emw-warp-mctf``
     - Warp Motion and CTF
     - WarpMctf
   * - ``emw-warp-tsalign``
     - Warp Tilt Series Alignment
     - WarpTsAlign
   * - ``emw-warp-ctfrec``
     - Warp CTF and Reconstruction
     - WarpCtfRec
   * - ``emw-warp-otf``
     - Warp OTF Preprocessing
     - WarpOtf
   * - ``emw-warp-export_particles``
     - Warp Export Particles
     - WarpExportParticles
   * - ``emw-warp-mtools_create``
     - Warp M Create Population
     - WarpMCreatePopulation
   * - ``emw-warp-mcore``
     - Warp MCore Refine
     - WarpMCore
   * - ``emw-warp-estimate_weights``
     - Warp Estimate Weights
     - WarpEstimateWeights
   * - ``emw-warp-mtools_resample``
     - Warp M Resample
     - WarpMResample

Relion
-------

Jobs wrapping native `Relion`_ programs, plus a couple of thin Relion-adjacent utilities.

.. list-table::
   :header-rows: 1
   :widths: 30 40 20
   :width: 100%

   * - Job
     - Label
     - Output
   * - ``relion.reconstructtomograms``
     - Relion Reconstruct Tomograms
     - Tomograms
   * - ``relion.pseudosubtomo``
     - Relion Extract Subtomograms
     - Extract
   * - ``relion.reconstructparticletomo``
     - Relion Tomo Reconstruct Particles
     - Reconstruct
   * - ``relion.initialmodel.tomo``
     - Relion Tomo Initial Volume
     - InitialModel
   * - ``relion.class3d.tomo``
     - Relion Tomo 3D Classification
     - Class3D
   * - ``relion.refine3d.tomo``
     - Relion Tomo Refine
     - Refine3D
   * - ``emw-relion-symmetrize_volume``
     - *(none -- falls back to the job id)*
     - --
   * - ``emw-relion-mask_create``
     - *(none -- falls back to the job id)*
     - --

PyTOM
------

Jobs wrapping `PyTOM`_ for 3D template matching.

.. list-table::
   :header-rows: 1
   :widths: 30 40 20
   :width: 100%

   * - Job
     - Label
     - Output
   * - ``emw-pytom-create_template``
     - PyTom Create Template
     - PyTom
   * - ``emw-pytom``
     - PyTom Template Matching
     - PyTom

AreTomo
--------

Jobs wrapping `AreTomo`_.

.. list-table::
   :header-rows: 1
   :widths: 30 40 20
   :width: 100%

   * - Job
     - Label
     - Output
   * - ``emw-aretomo3``
     - Aretomo3
     - Aretomo3
   * - ``emw-denoiset``
     - DenoisET Pipeline
     - DenoisET
