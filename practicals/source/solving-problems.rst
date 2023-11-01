Solving Common UM Problems
==========================
   
This section exposes you to more typical UM errors and hints at how to find and fix those errors.

You may encounter other errors, often as a result of mistyping, for which solution hints are not provided.

Set up N96 GA7.0 AMIP example suite
-----------------------------------

Find and make a copy of suite ``u-cc654``.

Firstly make the essential changes required to run the suite.  That is:

* The account code ('n02-training' if you're on an organised training event)
* Your ARCHER2 user name
* The queue to run in.

.. Hint::
   Look in the :guilabel:`suite conf` section.  For organised training events you will see that this suite is setup to use reservations listed as Tuesday, Wednesday, Thursday; select the appropriate day.  For self-study switch off "Use a reservation on ARCHER2" and select the ``short`` queue.

* Did you manage to find where to set your ARCHER2 username?  

This suite is set up slightly differently to the one used in the previous sections; suites do vary on how they are set up but you will soon learn where to look for things.  This suite is set up so that specifying your username on the remote HPC is optional. 

* Click :guilabel:`View --> View Latent Variables`. You should see ``Username on ARCHER2`` appear in the panel greyed out.
* Click the :guilabel:`+` sign next to it and select :guilabel:`Add to configuration`
* Enter your ARCHER2 username

Errors resolved in the code extraction
--------------------------------------

:guilabel:`Save` the suite and then :guilabel:`Run` it either from the GUI or the command line.

The suite should fail in the ``fcm_make_um`` task. This is the task that extracts all the required code from the repository including any branches.  The failure will be indicated in the Cylc GUI with a red square and the state ``failed``.  

* What is the error? 

.. 
   Examine the ``job.err`` and ``job.out`` to find the cause of the problem. You can view these files through Rose Bush, as we have done previously, however you can also view them quickly and easily directly from the Cylc GUI.  **Right-click** on the failed ``fcm_make_um`` task and select :guilabel:`View -> job stderr`

.. hint::
   Examine the ``job.err`` and ``job.out`` to find the cause of the problem. You can view these files quickly and easily directly from the Cylc GUI.  **Right-click** on the failed ``fcm_make_um`` task and select :guilabel:`View -> job stderr`

This indicates that the branch cannot be found due to an incorrect branch name. You will need to look at the UM code repository through Trac on MOSRS (https://code.metoffice.gov.uk/trac/um/browser) to determine the correct name.

Fix the error, :guilabel:`Save` the suite.

Now we will stop the suite and then re-run it.  In the Cylc GUI click on :guilabel:`Control > Stop Suite` and then select :guilabel:`Stop now` and then click on :guilabel:`OK`.  :guilabel:`Run` the suite again.

The suite will fail in the ``fcm_make_um`` task again.

* What is the error?

.. Hint::
   Again look in the ``job.err`` file.  This kind of error results when changes made in two or more branches affect the same bit of code and which the FCM system cannot understand how to resolve.

* Which file does the problem occur in?

In practice, you will need to fix the problem with the code conflict as you did in the FCM tutorial section.  To proceed in this case, navigate to :guilabel:`fcm_make_um --> sources` and remove the branch called ``vn11.7_training_merge_error`` by clicking on it and then clicking the :guilabel:`-` sign.

:guilabel:`Save` the suite.

Last time we stopped the suite and then re-ran it, however, it is possible to reload the suite definition and then re-trigger the failed task without first stopping the running suite. To do this change to the suite directory: ::

  puma2$ cd ~/roses/<suitename>

We then reload the suite definition by running the following Rose command: ::

  puma2$ rose suite-run --reload

Wait for this command to complete before continuing. Finally in the Cylc GUI *right-click* on the failed task and select :guilabel:`Trigger (run now)`.  The ``fcm_make_um`` task will then submit again.

* Is there an error in ``fcm_make_um`` this time?

If you look in the ``job.err`` file now it should be empty and the ``job.out`` file indicates SUCCESS.

Errors resolved in the compile and run
--------------------------------------

* Has the ``fcm_make2_um`` (compilation) task completed successfully?
* You should have a failure.  Open the ``job.err`` file - what does it indicate?
* Which routine has an error?
* What is the error?
* What line of the Fortran file does it occur on?

In practice, you would need to fix the error in your branch on PUMA and then restart the suite.  In this case, navigate to :guilabel:`fcm_make_um --> sources` and remove the branch ``vn11.7_training_compile_error``.  :guilabel:`Save` the suite, :guilabel:`Shutdown` or :guilabel:`Stop` the failed run and then :guilabel:`Run` it again.

.. tip::
   This time we chose to shutdown the failed suite rather than do a reload.  In this scenario we need to redo the code extraction (``fcm_make_um``) step so doing a reload would be slightly more complex; you would need to :guilabel:`Reload` and then :guilabel:`Re-trigger` both the ``fcm_make_um`` and the ``fcm_make2_um`` tasks.  With experience you get to know when it's better to do a :guilabel:`Reload` and when to :guilabel:`Shutdown`  a suite.

Note again that the task submitted successfully.  

* Did the ``fcm_make2_um`` task succeed this time?
* What about the ``install_cold`` task?
* What is the error?
* Does the start dump exist?
* What is the name of the correct start dump?

.. Hint::
   Look in the directory where it thinks the start file should be - is there a candidate in there?

Point your suite to the correct start dump.  Fixing this problem isn't quite as easy as it sounds.  A search in the Rose edit GUI for the dump file name ``ab642a.da19880901_00_err`` will not locate anything.  For this suite it is not possible to fix this issue through the GUI, for some other suites you can edit the initial dump location in the panel :guilabel:`um --> namelist --> Reconfiguration and Ancillary Control --> General technical options`.

Suites can be and are set up differently and there will be times when you need to edit the cylc suite definition files directly.

In your suite directory on PUMA (``~/roses/<suitename>``) use ``grep -R`` to search for the start dump name ``ab642a.da19880901_00_err`` in the suite files.  You should see 2 occurrences listed ::

  ros@puma2$ grep -r ab642a.da19880901_00_err *
  site/archer2.rc:{% set AINITIAL = AINITIAL_DIR + 'N96L85/ab642a.da19880901_00_err' %}
  site/meto_cray.rc:{% set AINITIAL = AINITIAL_DIR + 'N96L85/ab642a.da19880901_00_err' %}

Edit the dump name in the appropriate ``.rc`` file for the HPC we are running on, to point to the correct initial dump file.

.. Hint::
   This suite is set up to run on multiple platforms, make sure you edit the file appropriate to ARCHER2. You may notice that ``AINITIAL`` is set 3 times; a different file is required depending on the resolution the model is being run at.  This suite is running at N96 resolution.

:guilabel:`Reload` the suite definition and then :guilabel:`Re-trigger` the ``install_cold`` task.  The task should succeed this time.

* Has the model run successfully?

This time the model should have failed with an error.

* What is the error message?

.. Hint::
   Try searching for ``ERROR`` - you will soon learn common phrases to help track down problems.

.. note:: If you use the search ``job.err`` box at the bottom of the gcylc viewer, when you select :guilabel:`Find Next` you will see a message indicating the live feed will be disconnected. Click :guilabel:`Close`.

* Which PE Ranks signalled the Abort?

In general it can be useful to note which processors failed and then look at the detailed output for those processors. In this scenario, however, all the processors aborted.  We'll now take a look at the individual PE output file. Change to the ``pe_output`` directory for the atmos_main task. This is under ``~/cylc-run/<suite-id>/work/<cycle>/atmos_main/pe_output``. 

Open the file called ``<suite-id>.fort6.pe0``.  Sometimes extra information about the error can be found in the individual PE output files.
   
* At what timestep did the error occur?
   
The error message indicates that the model has suffered a convergence failure in the routine ``EG_BICGSTAB_MIXED_PREC``. This basically means that the model was not able to find a solution to the requested accuracy with the amount of effort specified. In this case the failure results from the value chosen for ``gcr_max_iterations``.  You could try to find what setting similar models use (with the MOSRS repository you have access to all model setups) or looking at the help within ``rose edit`` may point you in the right direction.  Go to :guilabel:`um --> namelist --> UM Science Settings --> Sections 10 11 12 - Dynamics settings -->  Solver` and set it to the suggested value. :guilabel:`Save`, :guilabel:`Reload` and :guilabel:`Re-trigger`.

The model should fail with the same error.  So what's gone wrong here?  We've changed the value of the number of iterations to a recommended value so why didn't it work?  The first thing to check is that the new value has indeed been passed to the model.  We do this by checking the variable in the namelists which are written by the Rose system. On ARCHER2 navigate to the work directory for the ``atmos_main`` task (ie. ``~/cylc-run/<suite-id>/work/<cycle>/atmos_main``).  In here you will see several files with uppercase names (e.g. ``ATMOSCNTL``, ``SHARED``), these contain the Fortran namelists which are read into the model.  Have a look inside one of them to see the structure.  Now search (use `grep`) in these files for the max number of solver iterations variable ``gcr_max_iterations``.

.. Hint::
   Search for the string ``gcr_max_iterations=``.

* What value does it have?  Is this what you changed it to in the Rose edit GUI?

So why was the change not picked up?  Go back to view the setting in the Rose GUI.  By the side of the variable ``gcr_max_iterations`` there is a little icon of a hand on paper, this indicates that there is an *"optional configuration override"* for this variable.

Optional configuration overrides add to or overwrite the default configuration. They are useful to make it easier to switch between different configurations of the model.  For example switching between different resolutions.

Click on the icon and the list of overrides appears.  You will see that the variable is set to 1 in the *training* override file and it is this value that is being used in the model.  Unfortunately optional configuration override files cannot be changed through the GUI so we will need to edit the Rose file directly. Override files for the ``um`` app live in the directory ``~/roses/<suite-id>/app/um/opt``.  Open the file ``rose-app-training.conf`` and edit the value for ``gcr_max_iterations``. :guilabel:`Save`, :guilabel:`Reload` and :guilabel:`Re-trigger` the suite.

Check the ``gcr_max_iterations`` variable in the namelist file again to confirm that it does now have the correct value. This time the model should run successfully. Check the output to confirm that there are no errors.  Check that the model converged at all time steps.













