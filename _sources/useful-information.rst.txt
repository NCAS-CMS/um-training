Appendix A: Useful information
==============================

UM output
---------

**ARCHER2 job output directory:**

The standard output and error files (job.out & job.err) for the compile, reconfiguration and run are written to the directory: ::

  ~/cylc-run/<suite-id>/log/job/<cycle>/<app>

**ARCHER2 model output:**

By default the UM will write all output (e.g. processor output and data files) to the directory it was launched from, which will be the task’s **work** directory. However, all output paths can be configured in the GUI and in practice most UM tasks will send output to one or both of the suite’s **work** or **share** directories: ::

  ~/cylc-run/<suitename>/work/1/atmos
  ~/cylc-run/<suitename>/share/data

ARCHER2 architecture
--------------------

ARCHER2 has two kinds of processor which we commonly use - they have several names, but roughly speaking they are the service processors (several nodes worth) sometimes referred to as the front end, and the compute processors (many many nodes worth) sometimes referred to as the back end. We login to the front end and build the model on the front end. We run the model on the back end. You wouldn't generally have an interactive session on the back end and will submit jobs there through the batch scheduler (PBS). 

The UM infrastructure recognises this architecture and will run tasks in the appropriate place. 

If you are doing any post-processing or analysis you may wish to submit your own parallel or serial jobs. Intensive interactive tasks should be run on the post-processor nodes. For analysing data on the /nerc disk, use the RDF cluster. 

Consult the ARCHER2 documentation for details (See www.archer2.ac.uk). 

ARCHER2 file systems
--------------------

ARCHER2, in common with some other HPC systems, such as MONSooN and Polaris, has (at least) two file systems which have different properties, different uses, different associated policies and different names. On ARCHER there are ``/home`` and ``/work``. The ``/home`` file system is backed up regularly (only for disaster recovery), has relatively small volume, can efficiently handle many small files, and is where we recommend the UM code is saved and built. The ``/home`` system can not be accessed by jobs running on the compute processors.

The ``/work`` file system is optimized for fast parallel IO - it doesn't handle small files very efficiently. It is where your model will write to and read from.

ARCHER2 node reservations
-------------------------

In normal practice you will submit your jobs to the parallel queue on ARCHER; the job scheduler will then manage your job request along with all those from the thousands of other users. For this training course, we will be using processor Reservations, whereby we have exclusive access to a prearranged amount of ARCHER2 resource meaning that you will not need to wait in the general ARCHER2 queues. Reservations are specified by a reservation code - e.g. n02-training_266. As an ARCHER2 user you can make a reservation so that you have access to the machine at a time of your choosing - reservations incur a cost overhead (50%), so best used when you are sure you need them.

Useful Rose commands
--------------------

``rose suite-run`` 

  Run a suite.

``rose suite-run --new`` 

  Clear out any existing cylc-run directories for this suite and then run it.  Take care when using this option as it deletes all files from any previous runs of the suite.

``rose suite-run --no-log-archive`` 

  Do not archive (tar-gzip) old log directories.

``rose suite-run --restart`` 

  Restart the suite from where it finished running previously

``rose suite-run [--restart] -- --hold`` 

  Hold (don't run tasks) immediately on running or restarting the suite 

``rose suite-shutdown`` 

  Shutdown (stop) a running suite.

``rose sgc`` 

  Launch the Cylc GUI for a running suite.

``rose suite-scan`` 

  Scan for any running suites.  This is useful when you've shutdown the cylc GUIs and wish to quickly see what suites you still have running.

For more information on all these commands and more see the Rose and Cylc documentation or run ``rose command --help`` (E.g. ``rose suite-run --help``) to view the man pages.

Problems shutting down suites
-----------------------------

**Types of shutdown**

By default when you try to shutdown a suite, cylc will wait for any currently running tasks to finish before stopping, which may not be what you want to do. You can also tell cylc to kill any active processes or ignore running processes and force the suite to shutdown anyway. The latter is what you will need to do if the suite has got stuck: ::

  rose suite-shutdown -- --now

To access these options in the cylc GUI, go to *"Control" -> "Stop Suite"*. See also ``rose help suite-shutdown`` for further details.

**Forcing shutdown**

Sometimes after trying to shutdown a suite, it will still appear to be running.

First make sure you have used the correct shutdown command and aren't waiting for any unfinished tasks (see above). It can take cylc a little while to shut down everything properly, so be patient and give it a few minutes.

If it still appears to be running (for example you get an error when you try to re-start the suite), you may have to do the following:

* Manually kill the active processes:

  Get a list of processes associated with the suite. For example, for suite u-ak194 you would run: ::

    puma u-ak193$ ps -flu annette  | grep u-ak194
    0 S annette   2735  5230  ... grep u-ak194
    1 S annette  18713     1  ... python /home/fcm/cylc-6.11.4/bin/cylc-run u-ak194
    1 S annette  18714 18713  ... python /home/fcm/cylc-6.11.4/bin/cylc-run u-ak194
    1 S annette  18715 18713  ... python /home/fcm/cylc-6.11.4/bin/cylc-run u-ak194
    1 S annette  18717 18713  ... python /home/fcm/cylc-6.11.4/bin/cylc-run u-ak194
    1 S annette  18718 18713  ... python /home/fcm/cylc-6.11.4/bin/cylc-run u-ak194

  This gives a list of processes. The number in the 4th column is the process-id. Use this to kill each of the processes, eg: ::

    kill -9 18713

* Delete the port file:
 
  This lives under ``~/.cylc/ports/``. For example: ``rm ~/.cylc/ports/u-ak194``
