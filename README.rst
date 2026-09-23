EMhub-Tomo Documentation
========================

This repository contains the documentation for **EMhub-Tomo**, a platform for CryoET data
processing that runs heterogeneous pipelines (Warp, Relion, PyTOM, AreTomo, ...) in a
flexible and structured way. It is built on the **emwrap** library for running external
programs, keeps processing projects compatible with Relion's data model, and provides a web
interface, based on **emhub** and **ScipionWeb**, for running pipelines and visualizing
results.

The documentation is live at https://3dem.github.io/emhub-tomo/

Building locally
----------------

The pages are written in reStructuredText under ``source/`` and built with Sphinx:

.. code-block:: bash

   pip install sphinx furo myst-parser
   make html    # output in build/html

Every push to ``main`` rebuilds and deploys the site to GitHub Pages
(see ``.github/workflows/deploy.yml``).
