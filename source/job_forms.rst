Job Forms
===========

Every job type ships its own ``form.json`` file (in ``emwrap/config/forms``) describing the parameters shown to the user for that job and how they are laid out in the Form UI. A form is a JSON object with a top-level ``sections`` array; each section groups related parameters under a label, often shown as a separate tab or framed box. Each parameter in a section is itself a JSON object whose ``paramClass`` selects the UI control to render -- a text field, a checkbox, a dropdown, and so on -- alongside common attributes like ``name``, ``label``, ``default``, and ``help``. Two special ``paramClass`` values, ``Line`` and ``Group``, nest and lay out other parameters instead of rendering a control of their own.

The full reference below is converted from ``emwrap/config/forms/README.md``.

File Structure
----------------

A form is defined by a single JSON file. The root of the JSON object must contain a ``sections`` array.

.. code-block:: json

   {
       "sections": [
           // ... one or more section objects
       ]
   }

Sections
~~~~~~~~~~

The ``sections`` array contains one or more section objects. Each section represents a grouping of parameters in the UI, often displayed as a separate tab or a framed box.

A section object has the following properties:

* ``label`` (string): The title of the section, displayed in the UI.
* ``params`` (array): An array of parameter objects that will be displayed in this section.

.. code-block:: json

   {
       "label": "Section Title",
       "params": [
           // ... one or more parameter objects
       ]
   }

Parameter Definitions
------------------------

Each object in the ``params`` array defines a single graphical parameter or UI element.

Common Attributes
~~~~~~~~~~~~~~~~~~~

Most parameter types share these common attributes:

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Attribute
     - Type
     - Description
   * - ``name``
     - string
     - The internal name of the parameter. This is used to identify the parameter and its value.
   * - ``label``
     - string
     - The display name for the parameter in the UI.
   * - ``default``
     - any
     - The default value for the parameter.
   * - ``help``
     - string
     - A help text or tooltip that provides more information about the parameter.
   * - ``paramClass``
     - string
     - The type of the graphical parameter. See supported parameter types below.
   * - ``pointerClass``
     - string
     - (Optional) Special attribute to define a "class" (beyond the actual value) that this parameter represents, kind of a "meta class". For example, a StringParam that points to an input particles STAR file can define its pointerClass as 'Particles'.

Additional Attributes
~~~~~~~~~~~~~~~~~~~~~~~

Besides the common attributes, some other attributes can be defined:

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Attribute
     - Type
     - Description
   * - ``condition``
     - string
     - Condition to be evaluated with other
   * - ``validators``
     - string
     - Most of the params have default validators (see sections below), but additional validations can be defined.
   * - ``allowsEmpty``
     - boolean
     - By default, a value should be set for each param. If this property is ``true``, empty values are allowed.
   * - ``readOnly``
     - boolean
     - If ``true``, the param will be displayed in the UI, but the user can not be modified.
   * - ``hidden``
     - boolean
     - Param will not be displayed, but it will be included in the job values dictionary.
   * - ``tableMin``, ``tableMax``
     - integer
     - Define these two attributes to create a Table of the given parameter type.

Supported Parameter Types
----------------------------

The ``paramClass`` attribute determines the type of graphical control to display. Here are the supported types:

``LabelParam``
~~~~~~~~~~~~~~~~

A simple text label, used for displaying information or titles within a form section.

**Example:**

.. code-block:: json

   {
       "name": "label_input",
       "label": "Input / Reference",
       "paramClass": "LabelParam"
   }

``StringParam``
~~~~~~~~~~~~~~~~~

A standard text input field.

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Attribute
     - Type
     - Description
   * - ``pattern``
     - string
     - Can be used to specify a file-browsing pattern, e.g., ``"STAR Files (*.star)"``.

**Example:**

.. code-block:: json

   {
       "name": "fn_in_raw",
       "label": "Raw input files:",
       "paramClass": "StringParam",
       "default": "Micrographs/*.tif",
       "pattern": "Movie or Image (*.{mrc,mrcs,tif,tiff,eer})",
       "help": "Provide a Linux wildcard that selects all raw movies or micrographs to be imported."
   }

``IntParam``
~~~~~~~~~~~~~~

A field for entering integer values.

**Example:**

.. code-block:: json

   {
       "name": "log_diam_min",
       "label": "Min. diameter for LoG filter (A)",
       "default": 200,
       "paramClass": "IntParam",
       "help": "The smallest allowed diameter for the blob-detection algorithm."
   }

``FloatParam``
~~~~~~~~~~~~~~~~

A field for entering floating-point values.

**Example:**

.. code-block:: json

   {
       "name": "acq.cs",
       "label": "Spherical Aberration (mm)",
       "default": 2.7,
       "valueClass": "Float",
       "paramClass": "FloatParam",
       "help": ""
   }

``BooleanParam``
~~~~~~~~~~~~~~~~~~

A checkbox for true/false values.

**Example:**

.. code-block:: json

   {
       "name": "do_log",
       "label": "OR: use Laplacian-of-Gaussian?",
       "default": false,
       "valueClass": "Boolean",
       "paramClass": "BooleanParam",
       "help": "If set to Yes, a Laplacian-of-Gaussian blob detection will be used."
   }

``EnumParam``
~~~~~~~~~~~~~~~

A dropdown menu (combobox) for selecting from a list of options.

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Attribute
     - Type
     - Description
   * - ``choices``
     - array or dict
     - If choices is a list, the items will be displayed and used as the selected value. If it is a dict, the keys will be used for the value.
   * - ``display``
     - string
     - The display style, e.g., ``"combo"``.

**Example:**

.. code-block:: json

   {
       "name": "ts_export_type",
       "label": "Export type: ",
       "paramClass": "EnumParam",
       "choices": ["2d", "3d"],
       "display": "combo"
   }

Grouping Elements
--------------------

``Line``
~~~~~~~~~~

A special parameter that groups other parameters to be displayed on a single line in the UI.

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Attribute
     - Type
     - Description
   * - ``params``
     - array
     - An array of parameter objects to be displayed on the same line.

**Example:**

.. code-block:: json

   {
       "paramClass": "Line",
       "label": "Resolution range:",
       "params": [
           {
               "name": "ts_ctf.range_low",
               "label": "low",
               "default": 30,
               "paramClass": "FloatParam",
               "help": "Minimum resolution in Angstrom to consider in fit"
           },
           {
               "name": "ts_ctf.range_high",
               "label": "high",
               "default": 4,
               "paramClass": "FloatParam",
               "help": "Maximum resolution in Angstrom to consider in fit"
           }
       ]
   }

``Group``
~~~~~~~~~~~

A special parameter that groups other parameters to be displayed on a grouped section.

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Attribute
     - Type
     - Description
   * - ``params``
     - array
     - An array of parameter objects to be displayed on the group.

**Example:**

.. code-block:: json

   {
       "paramClass": "Group",
       "label": "Match binning:",
       "params": [
       {
           "name": "binningTM",
           "label": "Transformation matrix binning",
           "expertLevel": 0,
           "condition": null,
           "paramClass": "IntParam",
           "help": "Binning of the tilt series at which the transformation matrices were calculated.",
           "default": 13
       },
       {
           "name": "binningTS",
           "label": "Tilt-series binning",
           "expertLevel": 0,
           "condition": null,
           "paramClass": "IntParam",
           "help": "Binning of the tilt-series.",
           "default": 1
       }
       ]
   }

Special Cases
----------------

Unnamed Parameters
~~~~~~~~~~~~~~~~~~~~~

In some cases, you might find objects in the ``params`` array that do not have a ``name`` or ``paramClass``. These seem to be used for passing direct command-line arguments or setting default values. The keys of the object are treated as the argument flags.

**Example:**

This object sets default values for ``--tomogram-ctf-model`` and ``--rng-seed``.

.. code-block:: json

   {
       "--tomogram-ctf-model": "phase-flip",
       "--rng-seed": 420
   }

Empty Objects
~~~~~~~~~~~~~~~

An empty object ``{}`` can be used as a spacer in the UI to create a visual separation between parameters.
