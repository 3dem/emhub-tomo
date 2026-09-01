Cluster Queues
===============

After the program launchers, the next section is the definition of cluster queues. You can define as many queues as you need, and each queue can have a different template, submit command, and parameters.
The following is an example defining three queues: two of them use LSF and the third one uses SLURM. In one of the queues, it is possible to select the GPU type for the job.

.. code-block:: json

    "queues": [
        {
            "name": "cryoem",
            "template": "$SCRIPTS/lsf_template.sh",
            "submit": "$SCRIPTS/lsf_submit.sh {job_script}",
            "params": [
                {
                    "name": "queue_name",
                    "default": "cryoem",
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
