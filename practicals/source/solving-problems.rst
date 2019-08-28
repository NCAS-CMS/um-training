Solving Common UM Problems
==========================

This section exposes you to more typical UM errors and hints at how to find and fix those errors.

You may encounter other errors, often as a result of mistyping, for which solution hints are not provided.

Copy and set up N96 GA7.0 AMIP example suite
--------------------------------------------

Find and make a copy of suite **u-ba799**.

Firstly make the changes required to run the suite.  That is the account code ('n02-training'), your ARCHER user name and the queue to run in.  Hint: Look in the *suite.conf* section.  You will see that this suite has the queue reservations listed as Wednesday, Thursday, Friday; select the appropriate day.

* Did you manage to find where to set your ARCHER username?  

This suite is set up slightly differently to the one used in the previous sections; suites do vary on how they are set up but you will soon learn where to look for things.  This suite is set up so that specifying your username on the remote HPC is optional.  If your PUMA username is the same as your username on ARCHER, or if the remote username is set in your ``~/.ssh/config`` file Cylc will be able to submit your suite without having to explicitly set your username in the suite.  However, on this course, we are using training accounts on ARCHER so you will need to set the username.

* Click *View -> View Latent Variables*. You should see HPC_USER appear in the panel greyed out.
* Click the **+** sign next to it and select *Add to configuration*
* Enter your ARCHER training username (e.g. 'ncastr01')

Errors resolved in the code extraction
--------------------------------------

**Save** the suite and then **Run** it either from the GUI or the command line.

The suite should fail in the *fcm_make_um* task. This is the task that extracts all the required code from the repository including any branches.  The failure will be indicated in the *gcylc* GUI with a red square and the state *failed*.  

* What is the error? 

Hint: Examine the *job.err* and *job.out* to find the cause of the problem. You can view these files through Rose Bush, as we have done previously, however you can also view them quickly and easily directly from the Cylc GUI.  **Right-click** on the failed *fcm_make_um* task and select *View -> job stderr*

This indicates that the branch cannot be found due to an incorrect branch name. You will need to look at the UM code repository through Trac either on MOSRS (https://code.metoffice.gov.uk/trac/um/browser) or the PUMA mirror (https://puma.nerc.ac.uk/trac/um.xm/browser with username: guest1 and password: tra1n1ng or use your own) to determine the correct name.

Fix the error, **Save** the suite.

Now we will stop the suite and then re-run it.  In the Cylc GUI click on *Control -> Stop Suite* and then select **Stop now** and then click on **OK**.  **Run** the suite again.

The suite will fail in *fcm_make_um* again.

* What is the error?

Hint: Again look in the *job.err* file.  This kind of error results when changes made in two or more branches affect the same bit of code and which the FCM system cannot understand how to resolve.

* Which file does the problem occur in?

In practice, you will need to fix the problem with the code conflict as you did in the FCM tutorial section.  To proceed in this case, navigate to *fcm_make_um -> sources* and remove the branch called ``vn11.0_merge_error`` by clicking on it and then clicking the **-** sign.

**Save** the suite.

Last time we stopped the suite and then re-ran it, however, it is possible to reload the suite definition and then re-trigger the failed task without first stopping the running suite. To do this change to the suite directory: ::

  puma$ cd ~/roses/<suitename>

We then reload the suite definition by running the following Rose command: ::

  puma$ rose suite-run --reload

Wait for this command to complete before continuing. Finally in the Cylc GUI *right-click* on the failed task and select **Trigger (run now)**.  The *fcm_make_um* task will then submit again.

* Is there an error in *fcm_make_um* this time?

If you look in the *job.err* file now it should be empty and the *job.out* file indicates SUCCESS.

Errors resolved in the compile and run
--------------------------------------

* Has the *fcm_make2_um* (compilation) task completed successfully?
* You should have a failure.  Open the *job.err* file - what does it indicate?
* Which routine has an error?
* What is the error?
* What line of the Fortran file does it occur on?

In practice, you would need to fix the error in your branch on PUMA and then restart the suite.  In this case, navigate to *fcm_make_um -> sources* and remove the branch ``vn11.0_compile_error``.  **Save** the suite, **Shutdown/Stop** the failed run and then **Run** it again.  Notice we chose to shutdown the failed suite this time rather than do a reload.  In this scenario we need to redo the code extraction (*fcm_make_um*) step so doing a reload would be slightly more complex; you would need to *Reload* and then *Re-trigger* both the *fcm_make_um* and the *fcm_make2_um* tasks.  With experience you get to know when it's better to do a *Reload* and when to *Shutdown*  a suite.

Note again that the task submitted successfully.  

* Did the *fcm_make2_um* task succeed this time?
* What about the reconfiguration task?
* What is the error?
* Does the start dump exist?
* What is the name of the correct start dump?  Hint: look in the directory where it thinks the start file should be - is there a candidate in there?

Point your suite to the correct start dump.  Fixing this problem isn't quite as easy as it sounds.  A search for **ainitial** in the Rose edit GUI will take you to the *General reconfiguration options* panel.

* Can you see the problem?

The initial dump location is set with an environment variable: AINITIAL.  Suites can be and are set up differently and there will be times when you need to edit the cylc suite definition files directly.

In your suite directory on PUMA (``~/roses/<suitename>``) use ``grep -R`` to search for where the variable *AINITIAL* is set (If you are unfamiliar with using `grep` please ask for help).  Edit AINITIAL in the appropriate ``.rc`` file to point to the correct initial dump file.  (Hint: This suite is set up to run on multiple platforms, make sure you edit the file appropriate to ARCHER.) You may notice that AINITIAL is set 3 times; a different file is required depending on the resolution the model is being run at.  This suite is running at N96 resolution.

**Reload** the suite definition and then **Re-trigger** the reconfiguration task.  The reconfiguration should succeed this time.

* Has the model run successfully?

This time the model should have failed with an error.

* What is the error message?

Hint: Try searching for "ERROR" - you will soon learn common phrases to help track down problems.

.. note:: If you use the search ``job.err`` box at the bottom of the gcylc viewer, when you select *"Find Next"* you will see a message indicating the live feed will be disconnected. Click *Close*.

* At what timestep did the error occur?

* Which PE Rank(s) signalled the Abort?  Make a note of which one(s)

Change to the ``pe_output`` directory for the atmos_main task. This is under ``~/cylc-run/<suite-id>/work/<cycle>/atmos_main/pe_output`` and contains the output from each PE.

Open the file called ``<suite-id>.fort6.pe<pe noted above>``.  Sometimes extra information about the error can be found in the individual PE output files.

The error message indicates that NaNs (NaN stands for Not a Number and is a numeric data type representing an undefined or unrepresentable value) have occurred in the routine EG_BICGSTAB.  This basically means something in the model has become unstable and "blown up". In this case the failure results from an incorrect value for the solar constant *'sc'*.  You could try to find what setting similar models use (with the MOSRS repository you have access to all model setups) or looking at the help within ``rose edit`` may point you in the right direction.  Go to *um -> namelist -> UM Science Settings -> Planet Constants* and set it to the suggested value. **Save**, **Reload** and **Re-trigger**.

The model should fail with the same error.  So what's gone wrong here?  We've changed the value of the solar constant to a valid value so why didn't it work?  The first thing to check is that the new value has indeed been passed to the model.  We do this by checking the variable in the namelists which are written by the Rose system. On ARCHER navigate to the work directory for the *atmos_main* task (ie. ``~/cylc-run/<suite-id>/work/<cycle>/atmos_main``).  In here you will see several files with uppercase names (e.g. ATMOSCNTL, SHARED), these contain the Fortran namelists which are read into the model.  Have a look inside one of them to see the structure.  Now search (use `grep`) in these files for the solar constant variable `sc`.  Hint: search for the string "`sc=`".

* What value does it have?  Is this what you changed it to in the Rose edit GUI?

So why was the change not picked up?  Go back to view the setting in the Rose GUI.  By the side of the variable `sc` there is a little icon of a hand on paper, this indicates that there is an *"optional configuration override"* for this variable.

Optional configuration overrides add to or overwrite the default configuration. They are useful to make it easier to switch between different configurations of the model.  For example switching between different resolutions.

Click on the icon and the list of overrides appears.  You will see that the variable is set to 120000.0 in the *training* override file and it is this value that is being used in the model.  Unfortunately optional configuration override files cannot be changed through the GUI so we will need to edit the Rose file directly. Override files for the `um` app live in the directory ``~/roses/<suite-id>/app/um/opt``.  Open the file ``rose-app-training.conf`` and edit the value for ``sc``. **Save**, **Reload** and **Re-trigger** the suite.

Check the ``sc`` variable in the namelist file again to confirm that it does now have the correct value. This time the model should run successfully. Check the output to confirm that there are no errors.  Check that the model converged at all time steps.













