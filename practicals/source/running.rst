Running a UM suite on ARCHER2
=============================
   
ARCHER2 architecture
--------------------

In common with many HPC systems, ARCHER2 consists of different types of processor nodes: 

* **Login nodes:** This is where you land when you ssh into ARCHER2. Typically these processors are used for file management tasks.

* **Compute / batch nodes:** These make up most of the ARCHER2 system, and this is where the model runs. 

* **Serial / post-processing nodes:** This is where less intensive tasks such as compilation and archiving take place. 

ARCHER2 has two file systems: 

* **/home:** This is relatively small and is only backed up for disaster recovery. 

* **/work:** This is much larger, but is not backed up. Note that the batch nodes can only see the work file system. It is optimised for parallel I/O and large files. 

Consult the ARCHER2 website for more information: http://www.archer2.ac.uk 


Running a Standard Suite
------------------------

To demonstrate how to run the UM through Rose we will start by running a standard N48 suite at UM13.0.  

Copy the suite
^^^^^^^^^^^^^^
* In ``rosie go`` locate the suite with idx **u-cc519** owned by **rosalynhatcher**. 
* Right click on the suite and select :guilabel:`Copy Suite`.  

This copies an existing suite to a new suite id.  The new suite will be owned by you.  During the copy process a wizard will launch for you to edit the suite discovery information, if you wish.

A new suite will be created in the MOSRS rosie-u suite repository and will be checked out into your ``~/roses`` directory. 

Edit the suite
^^^^^^^^^^^^^^
* Open your new suite in the Rose config editor GUI.

Before you can run the suite you need to change the *userid*, *queue*, *account code* and *reservation*:

* Click on :guilabel:`suite conf --> jinja2` in the left hand panel
* Set ``HPC_USER`` (that's your ARCHER2 username)

If following the tutorial as part of an organised training event:  

* Set ``HPC_ACCOUNT`` to **'n02-training'**
* Set ``HPC_QUEUE`` to **'standard'**
* Ensure ``RESERVATION`` is set to **True**
* Set ``HPC_RESERVATION`` to be the reservation code for today. (e.g. **'n02-training_1055426'**)

If following the tutorial as self-study:

* Set ``HPC_ACCOUNT`` to the budget code for your project. (e.g. **'n02-cms'**)
* Set ``HPC_QUEUE`` to **'short'**  
* Set ``RESERVATION`` to **False**

.. admonition:: Notes
		
   * Quotes around the variable values are essential otherwise the suite will not run.
   * In normal practice you submit your suites to the parallel queue (either **short** or **standard**) on ARCHER2.
   * For organised training events, we use processor reservations, whereby we have exclusive access to a prearranged amount of ARCHER2 resource.  Reservations are specified by adding an additional setting called the reservation code; e.g. **n02-training_226**.

* Save the suite (:guilabel:`File > Save` or click the *down arrow* icon)

Run the suite
^^^^^^^^^^^^^
The standard suite will build, reconfigure and run the UM.  

* Click on the triangle symbol on the right end of the menu bar to run the suite. 

Doing this will execute the ``rose suite-run`` command (more on this later) and start the Cylc GUI through which you can monitor the progress of your suite graphically. The Cylc GUI will update as the job progresses.

Looking at the queues on ARCHER2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
While you're waiting for the suite to run, let's log into ARCHER2 and learn how to look at the queues.

Run the following command: ::

  squeue -u <archer2-user-name>

This will show the status of jobs you are running.  You will see output similar to the following: ::

  ARCHER2> squeue -u ros
        JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON) 
       148599  standard u-cc519.      ros  R       0:11      1 nid001001

At this stage you will probably only have a job running or waiting to run in the serial queue. Running ``squeue`` will show all jobs currently on ARCHER2, most of which will be in the parallel queues. 

Once your suite has finished running the Cylc GUI will go blank and you should get a message in the bottom left hand corner saying ``Stopped with succeeded``.

.. tip::
  Cylc is set up so that it *polls* ARCHER2 to check the status of the task, every 5 minutes.  This means that there could be a maximum of 5 minutes delay between the task finishing on ARCHER2 and the Cylc GUI being updated. If you see that the task has finished running but Cylc hasn't updated then you can manually poll the task by right-clicking on it and selecting :guilabel:`Poll` from the pop-up menu.

Standard Suite Output
---------------------

The output from a standard suite goes to a variety of places, depending on the type of the file.  On ARCHER2 you will find all the output from your run under the directory ``~/cylc-run/<suitename>``, where ``<suitename>`` is the name of the suite. This is actually a symbolic link to the equivalent location in your ``/work`` directory (E.g. ``/work/n02/n02/<username>/cylc-run/<suitename>``. 

Task output
^^^^^^^^^^^

.. note:: Rose Bush is a web-based tool for viewing the standard output and errors from suites. Unfortunately this does not work on the current puma server, so we need to browse the log files directly.

.. note:: To run Rose Bush on Monsoon run: ``firefox http://localhost/rose-bush``	  

On PUMA2, navigate to the cylc-run directory: ::

  cd ~/cylc-run/<suitename>
  ls 

You should see directories for each of the suites that you have run. Go to the suite you have just run and into the log directory: ::

  cd <suitename>/log/job/1
  ls 

You will see directories for each of the tasks in the suite. For this suite there are 4 tasks: ``fcm_make`` (code extraction), ``fcm_make2`` (compilation), ``recon`` & ``atmos``. Try looking in one of the task directories: ::

  cd recon/NN
  ls

Here ``NN`` is a symbolic link created by Rose pointing to the output of the most recently run. You will see several files in this directory. The ``job.out`` and ``job.err`` files are the first places you should look for information when tasks fail.

..
  Rose bush
  ^^^^^^^^^
 
  The standard output and errors from the suite can be easily viewed using Rose Bush.

  For suites submitted from PUMA2; in a browser navigate to: http://puma.nerc.ac.uk/rose-bush
  
  Enter your PUMA2 userid and click :guilabel:`Suites List`.  You should then see a list of all the suites you have run.  Click on :guilabel:`tasks jobs list` for the suite you have just run. You can examine the output of each task using the links, as well as see whether the suite contains failed tasks, or is currently running.  For this suite you should see output files for 4 tasks: ``fcm_make`` (code extraction), ``fcm_make2`` (compilation), ``recon`` & ``atmos``. The ``job.out`` and ``job.err`` files are the first places you should look for information when tasks fail.

Compilation output
^^^^^^^^^^^^^^^^^^
The output from the compilation is stored on the host upon which the compilation was performed.  The output from ``fcm_make`` is inside the directory containing the build, which is inside the ``share`` subdirectory.

``~/cylc-run/<suitename>/share/fcm_make/fcm-make2.log``

If you come across the word "failed", chances are your model didn't build correctly and this file is where you'd search for reasons why.

UM standard output
^^^^^^^^^^^^^^^^^^
The output from the UM scripts and the output from PE0 of the model are written to the ``job.out`` and ``job.err`` files for that task. Take a look at the ``job.out`` for the ``atmos`` task, by opening the following file:

``~/cylc-run/<suitename>/log/job/1/atmos/NN/job.out``

* Did the linear solver for the Helmholtz problem converge in the final timestep?
  
.. admonition::  Job Accounting
		 
  The ``sacct`` command displays accounting data for all jobs that are run on ARCHER2.  ``sacct`` can be used to find out about the resources used by a job. For example; Nodes used, Length of time the job ran for, etc.  This information is useful for working out how much resource your runs are using.  You should have some idea of the resource requirements for your runs and how that relates to the annual CU budget for your project.  Information on resource requirements is also needed when applying for time on the HPC.

  Let's take a look at the resources used by your copy of ``u-cc519`` run.

  * Locate the SLURM Job Id for your run.  This is a 6 digit number and can be found in the ``job.status`` file in the cylc task log directory.  Look for the line ``CYLC_BATCH_SYS_JOB_ID=`` and take note of the number after the ``=`` sign.


  Run the following command: ::

    sacct --job=<slurm-job-id> --format="JobID,JobName,Elapsed,Timelimit,NNodes"

  Where ``<slurm-job-id>`` is the number you just noted above.  You should get output similar to the following: ::

    ARCHER2-ex> sacct --job=204175 --format="JobID,JobName,Elapsed,Timelimit,NNodes"
           JobID    JobName    Elapsed  Timelimit   NNodes 
    ------------ ---------- ---------- ---------- --------
    204175       u-cc519.a+   00:00:23   00:20:00        1
    204175.batch      batch   00:00:23                   1 
    204175.exte+     extern   00:00:23                   1
    204175.0     um-atmos.+   00:00:14                   1    

  The important line is the first line.
  
  * How much walltime did the run consume?

  * How much time did you request for the task?

  * How many CUs (Accounting Units) did the job cost?

  .. hint:: 1 node hour currently = 1 CU. See the ARCHER2 website for information about the CU.

  There are many other fields that can be output for a job.  For more information see the Man page (``man sacct``).  You can see a list of all the fields that can be specified in the ``--format`` option by running ``sacct --helpformat``. 

Binary output - work and share
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default the UM will write all output to the directory it was launched from, which will be the task's ``work`` directory.  However, all output paths can be configured in the GUI and in practice most UM tasks will send output to one or both of the suite's ``work`` or ``share`` directories.

``~/cylc-run/<suitename>/work/1/atmos``

or

``~/cylc-run/<suitename>/share/data``

For this suite output is sent to the ``work`` directory. 

Change directory to the work space.

* What files and directories are present?

Model diagnostic output files will appear here, along with a directory called ``pe_output``. This contains one file for each processor, for both model and reconfiguration, which contain logging information on how the model behaved.

Open one of these files ``<suite-id>.fort6.peXX`` in your favourite editor. 

The amount of output created by the suite and written to this file can be controlled in the suite configuration (:guilabel:`um --> env --> Runtime Controls --> Atmosphere only`). For development work, and to gain familiarity with the system, make sure "Extra diagnostic messages" are output. Switch it on in this suite if it isn't already.

It is well worth taking a little time to look through this file and to recognise some of the key phrases output by the model. You will soon learn what to search for to tell you if the model ran successfully or not. Unfortunately, important information can be dotted about in the file, so just examining the first or last few lines may not be sufficient to find out why the model hasn't behaved as you expected. Try to find answers to the following:

* How many prognostic fields were read from the start file?
* How many boundary layer levels did you run with?
* What was the range of gridpoints handled by this processor?

Check the file sizes of the different file types. The output directory will contain start dumps, diagnostic output files and possibly a core dump file if the model failed and these usually have very different sizes.




