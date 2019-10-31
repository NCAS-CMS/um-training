Running a UM suite on ARCHER
============================

ARCHER architecture
-------------------

In common with many HPC systems, ARCHER consists of different types of processor nodes: 

* **Login nodes:** This is where you land when you ssh into ARCHER. Typically these processors are used for file management tasks.

* **Compute / batch nodes:** These make up most of the ARCHER system, and this is where the model runs. 

* **Serial / post-processing nodes:** This is where less intensive tasks such as compilation and archiving take place. 

* **Service nodes:** These are used to launch the batch jobs amongst other things. 

ARCHER has three file systems: 

* **/home:** This is relatively small and is only backed up for disaster recovery. 

* **/work:** This is much larger, but is not backed up. Note that the batch nodes can only see the work file system. It is optimised for parallel I/O and large files. 

* **/nerc:** This is the Research Data Facility (RDF) used to archive data. It is backed up. 

Consult the ARCHER website for more information: http://www.archer.ac.uk 


Running a Standard Suite
------------------------

To demonstrate how to run the UM through Rose we will start by running a standard N48 suite at UM10.5.  

**i. Copy the suite**

* In ``rosie go`` locate the suite with idx **u-ag263** owned by **annetteosprey**. 
* Right click on the suite and select ``Copy Suite``.  

This copies an existing suite to a new suite id.  The new suite will be owned by you.  During the copy process a wizard will launch for you to edit the suite discovery information, if you wish.

A new suite will be created in the MOSRS rosie-u suite repository and will be checked out into your ``~/roses`` directory. 

**ii. Edit the suite**

* Open your new suite in the Rose config editor GUI.

Before you can run the suite you need to change the *userid*, *queue* and *account code*. 

Now make the following changes:

* Click on *suite conf -> jinja2* in the left hand panel
* Change HPC_USER (that's your ARCHER training account)
* Change HPC_ACCOUNT to **'n02-training'**
* Change HPC_QUEUE to be the reservation code for today. (e.g. **'R6585903'**)
* Save the suite (*File -> Save* or click the *down arrow* icon)

.. note:: Quotes around the 'n02-training', reservation code and your ARCHER username are essential otherwise the suite won't run.

.. note:: In normal practice you submit your suites to the parallel queue (either 'short' or 'standard') on ARCHER.  For this training course, we are using processor Reservations, whereby we have exclusive access to a prearranged amount of ARCHER resource.  Reservations are specified by a reservation code; e.g. R5212096.

**iii. Run the suite**

The standard suite will build, reconfigure and run the UM.  

* Click on the triangle symbol on the right end of the menu bar to run the suite. 

Doing this will execute the ``rose suite-run`` command (more on this later) and start the Cylc GUI (gcylc) through which you can monitor the progress of your suite graphically. The cylc GUI will update as the job progresses.

**iv. Looking at the queues on ARCHER**

While you're waiting for the suite to run, let's log into ARCHER and learn how to look at the ARCHER queues.

Run the following command: ::

  qstat -u <archer-user-name>

This will show the status of jobs you are running.  You will see output similar to the following: ::

  ncastr01@eslogin005:~> qstat -u ncastr01

  sdb: 
                                                         Req'd  Req'd   Elap
  Job ID        Username Queue   Jobname  SessID NDS TSK Memory Time  S Time
  ------------ -------- -------- -------- ------ --- --- ------ ----- - -----
  3988630.sdb  ncastr01 S3979005 atmos.1-    --    1  24    --  00:20 R 00:10

At this stage you will probably only have a job running or waiting to run in the serial queue. Running qstat will show all jobs currently on ARCHER, most of which will be in the parallel queues. 

Another useful command is ``serialJobs``, which lists the jobs in the serial queue only. You will need to run ``module load anaconda`` before running the ``serialJobs`` command.  Try it now: ::

  ncastr01@eslogin005:~> module load anaconda
  ncastr01@eslogin005:~> serialJobs

Once your suite has finished running the Cylc GUI will go blank and you should get a message in the bottom left hand corner saying *'Stopped with succeeded'*.

Cylc is set up so that it *polls* ARCHER to check the status of the task, every 5 minutes.  This means that there could be a maximum of 5 minutes delay between the task finishing on ARCHER and the Cylc GUI being updated. If you see that the task has finished running but Cylc hasn't updated then you can manually poll the task by right-clicking on it and selecting **Poll** from the pop-up menu.

Standard Suite Output
---------------------

The output from a standard suite goes to a variety of places, depending on the type of the file.  On ARCHER you will find all the output from your run under the directory ``~/cylc-run/<suitename>``, where ``<suitename>`` is the name of the suite. This is actually a symbolic link to the equivalent location in your ``/work`` directory (E.g. ``/work/n02/n02/<username>/cylc-run/<suitename>``. 

**Rose bush**

The standard output and errors from the suite can be easily viewed using Rose Bush.

For suites submitted from PUMA; in a browser navigate to: http://puma.nerc.ac.uk/rose-bush

Enter your PUMA userid and click *"Suites List"*.  You should then see a list of all the suites you have run.  Click on *"tasks jobs list"* for the suite you have just run. You can examine the output of each task using the links, as well as see whether the suite contains failed tasks, or is currently running.  For this suite you should see output files for 4 tasks: fcm_make (code extraction), fcm_make2 (compilation), recon & atmos. The job.out and job.err files are the first places you should look for information when tasks fail.

.. note:: To run Rose Bush on Monsoon run: ``firefox http://localhost/rose-bush``

**Compilation output**

The output from the compilation is stored on the host upon which the compilation was performed.  The output from fcm_make is inside the directory containing the build, which is inside the `share` subdirectory.

``~/cylc-run/<suitename>/share/fcm_make/fcm-make2.log``

If you come across the word "failed", chances are your model didn't build correctly and this file is where you'd search for reasons why.

**Standard output**

The output from the UM scripts and the output from PE0 is placed in the ``log`` subdirectory. As we saw in Rose Bush stdout and stderr are written to 2 separate files. For a task named *atmos*, the output from the most recent run will be:

``~/cylc-run/<suitename>/log/job/1/atmos/NN/job.out``

And the corresponding error file is:

``~/cylc-run/<suitename>/log/job/1/atmos/NN/job.err``

Here ``NN`` is a symbolic link created by Rose pointing to the output of the most recently run *atmos* task.

Take a look at the ``job.out`` for the *atmos* task either on the command-line or through Rose Bush.

* How much walltime did the run consume?  Hint: go to the bottom of the file and find walltime.  

* Why does the phrase walltime appear twice?

* How much time did you request for the task?

* How many AUs (Accounting Units) did the job cost? Hint: 1 core hour currently = 15 AUs (You should have some idea of the resource requirements for your runs and how that relates to the annual AU budget for your project). See the ARCHER website for information about the AU.

* Did the linear solve for the Helmholtz problem converge in the final timestep?

* How many prognostic fields were read from the start file?


**Binary output - work and share**

By default the UM will write all output to the directory it was launched from, which will be the task's ``work`` directory.  However, all output paths can be configured in the GUI and in practice most UM tasks will send output to one or both of the suite's ``work`` or ``share`` directories.

``~/cylc-run/<suitename>/work/1/atmos``

or

``~/cylc-run/<suitename>/share/data``

For this suite output is sent to the ``work`` directory. 

Change directory to the work space.

* What files and directories are present?

Model diagnostic output files will appear here, along with a directory called ``pe_output``. This contains one file for each processor, for both model and reconfiguration, which contain logging information on how the model behaved.

Open one of these files ``<suite-id>.fort6.peXX`` in your favourite editor. 

The amount of output created by the suite and written to this file can be controlled in the suite configuration (*um -> env -> Runtime Controls -> Atmosphere only*). For development work, and to gain familiarity with the system, make sure "Extra diagnostic messages" are output. Switch it on in this suite if it isn't already.

It is well worth taking a little time to look through this file and to recognise some of the key phrases output by the model. You will soon learn what to search for to tell you if the model ran successfully or not. Unfortunately, important information can be dotted about in the file, so just examining the first or last few lines may not be sufficient to find out why the model hasn't behaved as you expected. Try to find answers to the following:

* How many boundary layer levels did you run with?
* What was the range of gridpoints handled by this processor?

Check the file sizes of the different file types. The output directory will contain start dumps, diagnostic output files and possibly a core dump file if the model failed) and these usually have very different sizes.




