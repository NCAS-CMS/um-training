Appendix A: Useful information
==============================

UM output
---------

**ARCHER2 job output directory:**

The standard output and error files (job.out & job.err) for the compile, reconfiguration and run are written to the directory: ::

  ~/cylc-run/<workflow-name>/run1/log/job/<cycle>/<app>

**ARCHER2 model output:**

By default the UM will write all output (e.g. processor output and data files) to the directory it was launched from, which will be the task’s **work** directory. However, all output paths can be configured in the GUI and in practice most UM tasks will send output to one or both of the suite’s **work** or **share** directories: ::

  ~/cylc-run/<workflow-name>/run1/work/1/atmos
  ~/cylc-run/<workflow-name>/run1/share/data

ARCHER2 architecture
--------------------

ARCHER2 has two kinds of processor which we commonly use - they have several names, but roughly speaking they are the service processors (several nodes worth) sometimes referred to as the front end, and the compute processors (many many nodes worth) sometimes referred to as the back end. We login to the front end and build the model on the front end. We run the model on the back end. You wouldn't generally have an interactive session on the back end and will submit jobs there through the batch scheduler (slurm). 

The UM infrastructure recognises this architecture and will run tasks in the appropriate place. 

If you are doing any post-processing or analysis you may wish to submit your own parallel or serial jobs. Intensive interactive tasks should be run on the post-processor nodes (note. these will be available when the full system is in service.) 

Consult the ARCHER2 documentation for details (See www.archer2.ac.uk). 

ARCHER2 file systems
--------------------

ARCHER2, in common with some other HPC systems, such as MONSooN, has (at least) two file systems which have different properties, different uses, different associated policies and different names. On ARCHER2 there are ``/home`` and ``/work``. The ``/home`` file system is backed up regularly (only for disaster recovery), has relatively small volume, can efficiently handle many small files, and is where we recommend the UM code is saved and built. The ``/home`` system can not be accessed by jobs running on the compute processors.

The ``/work`` file system is optimized for fast parallel IO - it doesn't handle small files very efficiently. It is where your model will write to and read from.

ARCHER2 node reservations
-------------------------

In normal practice you will submit your jobs to the parallel queue on ARCHER2; the job scheduler will then manage your job request along with all those from the thousands of other users. For this training course, we will be using processor Reservations, whereby we have exclusive access to a prearranged amount of ARCHER2 resource meaning that you will not need to wait in the general ARCHER2 queues. Reservations are specified by a reservation code - e.g. n02-training_266. As an ARCHER2 user you can make a reservation so that you have access to the machine at a time of your choosing - reservations incur a cost overhead (50%), so best used when you are sure you need them.

Cylc Cheat Sheet
----------------

Summary sheet covering most of the major Cylc commands for interacting with a workflow: https://cylc.github.io/cylc-doc/stable/html/user-guide/cheat-sheet.html

For convenience the basic cylc commands needed for this training are:

``cylc vip <workflow-name>``   
  Validates the workflow configuration, installs the workflow (ie. copy its files into the ``~/cylc-run`` directory) and start a workflow running.

``cylc play <workflow-name>``
  Start or Restart a workflow

``cylc stop [--now] <workflow-name>`` 
  Stop a workflow

``cylc vr <workflow-name>`` 
  Validate, reinstall and reload the workflow.  Used after making changes to a suite configuration

``cylc graph <workflow-name>``
  Generate a graphical representation of the workflow's graph

``cylc tui <workflow-name>`` 
  Open the in-terminal utility for monitoring and controlling a specific workflow



