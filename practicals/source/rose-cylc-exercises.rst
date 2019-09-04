Rose/Cylc Exercises
===================

Differencing suites
-------------------

Currently there is no Rose tool to difference two suites. Since a suite consists of text files it is simply a matter of making sure all the Rose configuration files are in the common format by running ``rose config-dump`` on each suite and then running ``diff``.

We will difference your copy of the GA7.0 suite with the original one: ::

  puma$ cd ~/roses
  puma$ rosie checkout u-ba799
  puma$ rose config-dump -C u-ba799
  puma$ rose config-dump -C <your-suitename>
  puma$ diff -r u-ba799 <your-suitename>

* Are the differences what you expected?

Graphing a suite
----------------

When developing suites, it can be useful to check what the run graph looks like after jinja evaluation, etc.  

The GA7.0 suite that we have been working with is very simple so we shall graph a nesting suite which is more complex. To do this without running the suite: ::

  puma$ rosie checkout u-ah076
  puma$ cd ~/roses/u-ah076
  puma$ rose suite-run -l --name=u-ah076 # install suite in local cylc db only
  puma$ cylc graph u-ah076               # view graph in browser

A window containing the graph of the suite should appear.

Exploring the suite definition files
------------------------------------

Change to the ``~/roses/<suite-id>`` directory for your copy of u-ag263.

Open the ``suite.rc`` file in your favourite editor.  

Look at the ``[scheduling]`` section.  This contains some Jinja2 variables (BUILD & RECON) which allow the user to select which tasks appear in the dependency graph. The dependency graph tells Cylc the order in which to run tasks.  The ``fcm_make`` and ``recon`` tasks are only included if the ``BUILD`` and ``RECON`` variables are set to true. These variables are located in the ``rose-suite.conf`` and can be changed using the rose edit GUI or by directly editing the ``rose-suite.conf`` file.  When you run a suite a processed version of the ``suite.rc`` file with all the Jinja2 code evaluated is placed in your suite's ``cylc-run`` directory.  

* Take a look at the ``suite.rc.processed`` file for your suite.  Hint: go to directory ``~/cylc-run/<suite-id>``.
* Change the values of BUILD and RECON and re-run your suite.  
* Look at the new ``suite.rc.processed`` file.  Can you see how the graph has changed?

Make sure that you leave the suite with BUILD=false before continuing.

As we saw earlier when changing the path to the start dump, some settings can't be changed through the rose edit GUI.  Instead you have to edit the suite definition files directly. 

* Can you find where the atmos processor decomposition is set for this suite?
* Change atmos processor decomposition to run on 2 nodes.  Run the suite.
* What error message did you get? Hint: Look in the usual ``job.out/job.err`` or it may be in the ``job-activity.log`` file.

This error is caused by a mismatch in the number of nodes requested by the PBS job script header and the number of processors requested by the ``aprun`` command which launches the executable. (For further information on PBS and the aprun command on ARCHER see: http://www.archer.ac.uk/documentation/user-guide/batch.php).

In the ``[[atmos]] [[[directives]]]`` section change ``-l select=1`` to ``-l select=2`` to tell the PBS scheduler that you require 2 nodes. 

* The suite should run this time. Did it run on 2 nodes as requested?
* How much walltime has been requested for the reconfiguration?

Now take a look at the ``suite.rc`` file for your other suite (the one copied from u-ba799). See how it differs.  This one is set up to run on multiple platforms.  

* Can you see the more complex dependency graph?
* Can you see where to change the reconfiguration walltime for this suite?

This has just given you a very brief look at the suite definitions files.  More information can be found in the cylc documentation.  

Suite and task event handling
-----------------------------

Suites can be configured to send emails to alert you to any task or suite failures (or indeed when the suite finishes successfully). To send an email, you use the built-in setting ``[[[events]]] mail events`` to specify a list of events for which notifications should be sent.  Here we will configure your copy of suite u-ba799 to send an email on task (submission) failure, retry and timeout. 

Edit the ``suite.rc`` file to add the ``[[[events]]]`` section below: ::

    [runtime]
        [[root]]
            ...
            [[[environment]]]
            ...
            [[[events]]]
                mail events = submission retry, retry, submission failed, failed, submission timeout, timeout
                submission timeout = P1D

Configure cylc so it knows what your email address is. Edit the file ``~/.cylc/global.rc`` (create it if it doesn't exist) to add the following: ::

   [task events] 
       mail to = <enter-your-email-address>

To test this out we need to force the suite to fail.  Change the account code to a non-existent one; e.g. 'n02-fail'

* Did you get an email when the suite failed?
* Look in the suite error files to find the error message?

Change the account code back to 'n02-training' before continuing.

Further information about event handlers can be found in the Cylc documentation: https://cylc.github.io/cylc/html/single/cug-html.html#13.15

Starting a suite in "held" mode
-------------------------------

This allows you to trigger the running of tasks manually.

To start a suite in held mode add ``-- --hold`` to the end of the ``rose suite-run`` command: ::

  puma$ rose suite-run -- --hold

The first ``--`` tells Rose that all subsequent options should be passed on to Cylc.  This is why the hold option should be added to the end of the command, after any Rose options.  Once the suite has started all tasks will be in a held state.  It is then possible to select which tasks are run by right clicking on a task in the Cylc GUI and manually triggering it or resetting its state.

Try doing this as a way to run the reconfiguration only in one of your suites.

Discovering running suites and the multi-suite monitor GUI
----------------------------------------------------------

Suites that are currently running can be detected with command line or GUI tools:

Submit 2 of your suites. It doesn't matter what tasks they are running for this exercise; compilation, recon or model run.

Now try running the command ``cylc scan``. This lists your currently running suites.  For example: ::

  puma$ cylc scan
  u-af140 ros@localhost:7770
  u-ag761 ros@localhost:7776

There is also a multi-suite monitor GUI, which allows you to monitor the states of all suites you have running in one window.  Try running the command: ::

  puma$ cylc gscan &

  Double clicking on a suite in *gscan* opens the *gcylc* window, which you will be very familiar with by now. For each suite open the *gcylc* window and stop the suite by going to *Control -> Stop Suite*, selecting  **Stop after killing active tasks** and clicking **Ok**.
  

Adding a new task to a suite
-------------------------------------

To add a new task, you have to specify how it relates to other tasks, specifically, which task will trigger it and which task will follow the new one.  Then  you have to specify the details of the task in the file ``rose-app.conf`` . This might require meta-data to be added to tell the general user what the inputs to the task mean. Any scripts needed to support your task can be added into the suite ``bin`` directory (for binary, or executable files). The suite configuration file suite.rc is the place where you modify the task graph.  Later in the same file you need to specify which computer will run the task and the resources it will need. 

In this example, we will add a task that says ``Hello, World`` which will execute after the reconfiguration and before the main model.

Begin by creating a new directory in the suite applications directory of your copy of u-ba799.  Close the Rose GUI first and the  go into the ``app`` directory and create a new directory called ``new_app``.  Change into the new directory and create a blank ``rose-app.conf file`` e.g. ``touch rose-app.conf``.

Now go to the top of the suite directory and start the Rose editor.  You should now see the new application listed.  At this point it is an empty application which does nothing and is not integrated into the task chain.  Click on the little triangle to the left of new_app to expand its contents (You may need to tick View -> View Latent Pages in the GUI to see this).  Everything is greyed out.  Click on ``command`` to see the command page and then click the plus sign and select “add to configuration” to add a command to the application.  Then enter ``echo Hello, World from new_app`` in the command default box.  Save this and then have a look at the contents of rose-app.conf to see the effect.

We will execute the new application after the reconfiguration and before the UM starts.  We will run it on ARCHER.  To set this up, edit the ``suite.rc`` file.  Under, ::

  [scheduling]
     [[dependencies]]

find the line  ``graph = recon  => atmos_main``
and change it to, ``graph = recon => new_app => atmos_main``.

This puts the new_app in the right place in the task list.

The next step is to tell Rose to run the application on ARCHER.  Under the section [runtime] there are environment definitions for [[recon]] and for [[atmos_main]].  Insert one for [[new_app]].  Since this is a simple command, it will be run in the serial queue.  The queuing system is specific to the super computer being used.  In our case, we want to make a modification to the ARCHER specific description which can be found in ``site/archer.rc``.  There is already a definition for the serial queue environment  [[HPC_SERIAL]] that we can make use of.   To run the new application on the ARCHER serial queue and allow it two minutes to complete, add the lines, ::

   [[new_app]]
       inherit = HPC_SERIAL
      [[[job]]]
            execution time limit = PT2M

after the environment for [[INSTALL_ANCIL_RESOURCE]].
	    
We are now ready to go.  Press run in the GUI and look at the task graph: recon and atmos_main are there, but a new hierarchy of tasks has appeared, ::

  HPC
      HPC_SERIAL
          new_app


Notice that ``atmos_main`` no longer runs after the reconfiguration, but ``new_app`` does and when that is completed, ``atmos_main`` starts, as we wanted. The output from ``new_app`` can be found in the Cylc output directory in ``log/job/19880901T0000Z/new_app/NN/job.out``.

A more complex application might involve the execution of a script.  In this case we would replace the contents of the command default box with the name of the script.  Then you would store the script in the suite bin directory, where it would become part of the suite (remember to ``fcm add`` any new files that you add to the suite so they will be added to the repository when you next commit).

Designing a new application may seem a daunting process, but there are numerous existing examples in suites that you can try to understand.  For to know more, see the Rose documentation at https://metomi.github.io/rose/doc/html/tutorial/rose/applications.html.  There are a collection of built-in applications that you can use for building, testing, archiving and housekeeping - see https://metomi.github.io/rose/doc/html/api/rose-built-in-applications.html.
