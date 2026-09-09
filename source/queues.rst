Cluster Queues
===============

After the program launchers, the next section is the definition of cluster queues. You can define as many queues as you need, and each queue can have a different template, submit command, and parameters.
The following is an example defining three queues: two of them use LSF and the third one uses SLURM. In one of the queues, it is possible to select the GPU type for the job.

.. code-block:: json

    "queues": [
        {
            "name": "cryo",
            "template": "$SCRIPTS/lsf_template.sh",
            "submit": "$SCRIPTS/lsf_submit.sh {job_script}",
            "params": [
                {
                    "name": "queue_name",
                    "default": "cryo",
                    "condition": "false"
                },
                {
                    "name": "gpu_type",
                    "label": "GPU type",
                    "help": "Select the GPU type if you need an specific one for this job.",
                    "default": "any",
                    "paramClass": "EnumParam",
                    "choices": ["any", "V100", "A100"]
                }
            ]
        },
        {
            "name": "cryo_core",
            "template": "$SCRIPTS/lsf_template.sh",
            "submit": "$SCRIPTS/lsf_submit.sh {job_script}",
            "params": [
                {
                    "name": "queue_name",
                    "default": "cryo_core",
                    "condition": "false"
                }
            ]
        },
        {
            "name": "rtx5000",
            "template": "$SCRIPTS/slurm_rtx5000_template.sh",
            "submit": "sbatch {job_script}",
            "params": [
                {
                    "name": "queue_name",
                    "default": "rtx5000",
                    "condition": "false"
                }
            ]
        }
    ]

The ``queue_name`` Parameter
------------------------------

Every queue **must** define a ``queue_name`` param. Its value is what gets substituted into the ``template`` and ``submit`` command (e.g. ``--partition={queue_name}`` for SLURM, or ``-q {queue_name}`` for LSF) to actually route the job to that destination queue on the cluster -- without it, the job script would have nowhere to go.

However, ``queue_name`` is set with ``"condition": "false"``, which hides it from the job submission form: since its value is fixed per-queue (via ``default``), there is nothing for the user to choose, so it is passed through automatically rather than shown as an option.

Additional Queue Parameters
-----------------------------

Besides ``queue_name``, a queue can define any number of extra params that *are* shown to the user in the job submission form, letting them pick job-specific options for that particular queue. In the example above, the ``cryo`` queue adds a ``gpu_type`` param (an ``EnumParam`` with choices ``any``, ``V100``, and ``A100``), so a user submitting to ``cryo`` can request a specific GPU type; its value is then available to the ``template``/``submit`` command as ``{gpu_type}``, just like ``queue_name``. The ``cryo_core`` and ``rtx5000`` queues in this example only define ``queue_name``, so no extra options are shown for them -- but nothing stops a queue from defining several such params, each with its own ``paramClass`` (``EnumParam``, ``StringParam``, ``IntParam``, etc. -- see :doc:`job_forms` for the full list of supported types).

Job Script Template
--------------------

For each queue, a submission template is required to create the job script for each job. The template is a bash script that will be executed by the cluster scheduler. All the parameters defined in the queue will be passed in
a dictionary to the template. Additional parameters that will be accessible to the template (and submit command) are:

* **jobId**: the project job id (and folder) not the scheduler job id
* **command**: the command to execute
* **gpu_line**: this is specific for LSF clusters, where CPU only jobs avoid the line for GPU requests.
* **job_id**: the job id
* **gpus**: number of GPUs requested by the job.
* **cpus**: number of CPUs requested by the job.
* **working_dir**: the working directory for the job (the project folder).
* **job_out**: the path to the job output file.
* **job_err**: the path to the job error file.

The following is an example of a SLURM template:

.. code-block:: bash

    #!/bin/bash

    #SBATCH --partition={queue_name}
    #SBATCH --nodes=1
    #SBATCH --tasks=1
    #SBATCH --cpus-per-task={cpus}
    #SBATCH --gres=gpu:{gpus}
    #SBATCH --mem=200G
    #SBATCH --output={job_out}
    #SBATCH --error={job_err}

    cd {working_dir}
    hostname -f
    {command}

And the following is an example of a LSF template:

.. code-block:: bash

    #!/bin/bash

    #BSUB -P emwrap-tomo
    {gpu_line}
    #BSUB -R "rusage[mem=5000]"
    #BSUB -q {queue_name}
    #BSUB -n {cpus}
    #BSUB -R "span[ptile={cpus}]"
    #BSUB -e {working_dir}/{jobId}/run.err -o {working_dir}/{jobId}/run.out

    cd {working_dir}
    hostname -f
    {command}
