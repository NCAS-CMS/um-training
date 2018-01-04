Further Exercises
=================

Now that we have built the suite, there is no need to rebuild it each time you run it.  Switch off compilation of the UM and reconfiguration.  Hint: See the *"suite conf"* section.

Change the model output logging behaviour
-----------------------------------------

Navigate to *um -> namelist -> Top Level Model Control -> Run Control and Time Settings*. Set **ltimer** to *true*.  Timer diagnostics outputs timing information and can be very useful in diagnosing performance problems.

**Save** and **Run** the suite.

Check the *job.out* file.

* Which routine took the most time?
* How many times was *Atm_Step* called?
* How many time steps did the model run for?
* Which PE was the slowest to run AP2 Boundary Layer? Which was the fastest?

Switch on "IO timing" Hint: look in *"IO System Settings"*.  

**Re-run** the model and search for "Total IO Timings" in the *job.out* file.

Change the processor decomposition
----------------------------------

Navigate to *suite conf -> Domain Decomposition -> Atmosphere*.

* What is the current processor decomposition?
* Why is this not a good way to run the model?

Hint: The base ARCHER charging unit is a node irrespective of how many cores on the node are being used. ARCHER has 24 cores per node, and for the UM each MPI task and OpenMP thread is mapped to a separate core.  So in this case we are running 8x10 (x 2 OMP threads) for a total of 160 cores, but are charged for 7 nodes (168 cores).

Try reducing the processor decomposition to 4(EW) x 3(NS). Run the model.

* What is the error?  

Using too few cores has resulted in the model failing due to insufficient memory, indicated by the message *"OOM killer terminated this process"*.  In this case it is easy to diagnose the problem, but sometimes it can be difficult to diagnose, so it's worth trying to increase the number of processors if you suspect memory resource issues. 

Try experimenting with different processor decompositions (E.g. 8x6, 12x12, etc)

* How do the timings compare to when you ran on 7 nodes?

You can come up with a performance vs processor count curve in this way which might be valuable if you are planning an experiment - it's also worth adding in the AU cost calculation when doing this.

.. note:: Running "under populated", i.e. with fewer than the total cores per node, gives access to more memory per parallel task.

Change the processor decomposition to run fully populated on 8 nodes with 2 OpenMP threads.

STASH
-----

**i. Exploring STASH**

Navigate to *um -> namelist -> Model Input and Output -> STASH Requests and Profiles*. Look at the time profiles called ``TALLTS`` and ``T1H``.

* What are they doing?

(``TALLTS`` says output on every timestep, ``T1H`` says output hourly)

Look also at some of the other time, domain and usage profiles.  The domain profiles determine spatial output and the usage profiles effectively specify a Fortran LUN (Logical Unit Number) on which the associated data is written.  

Click on *STASH Requests*. Now change the time profile for all stash output whose ``Usage`` profile is UPC and ``Time`` profile is T1H - to do this, click on each diagnostic you wish to change and then click the time profile, a drop-down list should appear containing all the available time profiles.  Select ``TALLTS``.  You can sort the STASH table to make it more convenient to make these changes.  Click on the ``use_name`` column header to sort by usage profile.

**ii. STASH validation macro**

Several Rose macros have been provided to help verify STASH setup.  When you change STASH it is always recommended to run at least the validate macro. The *stash_testmask.STASHTstmskValidate* macro ensures that the STASH output requsted is valid given the science configuration of the app.  To put this to the test run the STASH validation macro by selecting *stash_testmask.STASHTstmskValidate* from the list of available macros at the top of the STASH requests panel or alternatively it can be accessed from the *"Metadata -> um"* menu.  

You should see several errors reported - it appears we have asked for diagnostics which are not available.  This won't cause the model to fail, however, you could find these diagnostics in the list and switch them off by unchecking the "incl?" column, if you'd like to stop seeing this message.

**Save** and **Re-run** the suite.

The model should fail with an error message similar to the following:

  **STWORK: Number of fields exceeds reserved headers for unit  14**

This means that the number of output fields exceeds the limit set for a particular stream (the default is 4096 fields); in this case the stream attached to unit 14.  To find out what stream unit 14 is take a look in the ``job.out`` file and search for "unit 14". You should see that the file opened on unit 14 is <suite-id>a.pc19880901, so this is the **pc** stream.  Back in ``rose edit`` for this suite look at the STASH usage profile for **upc**.

* What is the file ID of the failing output stream?

Now navigate to the window for this stream under *Model Input and Output -> Model Output Streams*.  This defines the output stream.  You should see confirmation of the base output file name to be ``*.pc*``.  There are 2 ways to fix this problem:

1) Increase the **reserved_headers** size.

or

2) Change the reinitialisation frequency by modifying **reinit_step** and/or **reinit_unit**.  This is telling the model to create new output files at a specified frequency, so individual files don't get massively large.

Increasing the reserved header size is fine for smaller increases. Overriding the size by a large amount and thus having large numbers of fieldsfile headers can be inefficient for both runtime and memory. Thus the recommended way is to change the periodic reinitialisation of the fieldsfiles.  

Modify the reinitialisation frequency and run the model again. Take a look at the model output files. You should see that you have multiple ``*.pc19980901_*`` files.

**iii. Adding a new STASH request**

Let's now try adding a new STASH request to the UM app.

Click the "New" button in the STASH Requests section.  A window will appear in order for you to browse all available STASHmaster entries.

By default STASHmaster entries are grouped together by Section code. It is possible to group items by any of the STASHmaster codes using the Group drop down list. The View button contains options to display the STASHmaster entry values and/or the column titles with explanation text and to select which columns to show/hide.

Expand the *"Gravity wave drag"* section.  Then change the view by selecting *View -> Show expanded value info*. Try out the other options in the *View* menu to see what effect they have.

Select a STASH item and click **Add** to add it to the list of STASH requests.  In the STASH Requests panel click on the empty *dom_name*, *tim_name* and *use_name* fields of the new request and select appropriate profiles from the drop down lists.  These lists are populated from the entries of the time, use and domain namelists.

Once you have added a new STASH request, you need to run a macro to generate an index for the namelist.  To do so click on the **Macros** button, then select **stash_indices.TidyStashTransform**. A box will pop up listing the changes the editor is going to make, click **Apply**.

* Run the model.  Did it work?

Change the dump frequency
-------------------------

Set the model run length to 6 hours.  Hint: *suite conf -> Run Initialisation and Cycling*.

.. note:: Hours are represented in the ISO 8601 standard as *PT<num-hours>H* (e.g. PT1H represents 1 hour). Days are represented as P<num-days>D (e.g. P10D represents 10 days)

Reset the STASH output for stream UPC to hourly and the file reinitialisation frequency to 12 hourly.

Navigate to *um -> namelist -> Model Input and Output -> Dumping and Meaning*.

* What is the current dump frequency?

Set the dump frequency to 6 hours.  **Run** the model.

* What is the error?

This error message occurs when you have set the total run length to be less than the cycling (automatic resubmission) frequency.  Change the cycling frequency to 6 hours. Run the model.

* How much time was spent in DUMPCTL?

Set the dump frequency to 1 hour. **Run** the model.

* What happened to the time spent in DUMPCTL?

Reconfiguration
---------------

Try to find out how to run the reconfiguration only. Hint: Look in the *"suite conf"* section.

Try to find out where to request extra diagnostic messages for the reconfiguration output.

**Run** the reconfiguration only with extra diagnostic messages.

Look at the *job.out* file.

* Do you see a land-sea mask?

Setting up a suite to cycle
---------------------------

We mentioned in the presentations that the length of an integration will be limited by the time that a model is allowed to run on the HPC (see the ARCHER web pages for information about the time limits).  Clearly this is no good for much of our work which may need to run on the machine for several months.  Cylc and the UM allow for long integrations to be split up into multiple shorter jobs - this is called *cycling*.

Let's run the model for 3 hours with 1 hour cycling:

* Set the *"Total run length"* to 3 hours.
* Set the *"Cycling frequency"* to 1 hour.
* Set the *"Wallclock time"* to 10 minutes.
* Ensure that the model dump frequency is hourly, in this case.

**Save** and **Run** the suite.

.. note:: The automatic resubmission frequency must be a multiple of the dump frequency.

The model will submit the first cycle and once that has succeeded you will see the following 2 cycles submitted and run.

.. note:: It is always wise, particularly when you plan to run a long integration that you only run the first cycle initially so that you can check that the model is doing what you expected before committing to a longer simulation.

Restarting a suite
------------------

Let's now extend this run out to 6 hours.  Change the *"Total run length"* to 6 hours and **Save** the suite.

Having already run the first 3 hours we just want the suite to pick up where it left off and run the remaining 3 hours.  To do this we *restart* the suite, by typing: ::

  puma$ rose suite-run --restart

The cylc GUI will pop up and you should see the run resuming from where it left off (i.e. from cycle point 19880901T0300Z).

IO Servers
----------

Older versions of the UM did not have IO servers, which meant that all reading and writing of fields files went through a single processor (pe0).  When the model is producing lots of data and is running on many processors, this method of IO is very inefficient and costly - when pe0 is writing data, all the other processors have to wait around doing nothing but still consuming AUs.  Later UM versions, including UM 10.5, have IO servers which are processors dedicated to performing IO and which work asynchronously with processors doing the computation.

Here's just a taste of how to get this working in your suite.

Set the suite to run for 6 hours with an appropriate cycling frequency, then check that OpenMP is switched on (Hint: search for *openmp* in rose edit) as this is needed for the IO servers to work.

Navigate to *suite conf -> Domain Decomposition -> Atmosphere* and check the number of OpenMP threads is set to 2. Set the number of *"IO Server Processes"* to 8.

**Save** and then **Run** the suite.

You will see lots of IO server log files in ``~/cylc-run/<suitename>/work/<cycle>/atmos_main`` which can be ignored for the most part.

Try repeating the "Change dump frequency" experiment with the IO servers switched on - you should see much faster performance.

Running the coupled model
-------------------------

The coupled model consists of the UM Atmosphere model coupled to the NEMO ocean and CICE sea ice models.  The coupled configuration used for this exercise is N96 resolution for the atmosphere and a 1 degree ocean - you will see this written N96 ORCA1.

**i. Checkout and run the suite**

Checkout and open the suite **u-ak943**.  The first difference you should see is in the naming of the apps; there is a separate build app for the um and ocean, called *fcm_make_um* and *fcm_make_ocean* respectively. The model configuration is under *coupled* rather than *um*.

Make the usual changes required to run the suite (i.e. set username, account code, queue)

Check that the suite is set to build both the UM and ocean, as well as run the reconfiguration and model.

**Run** the suite.

**ii. Exploring the suite**

Whilst the suite is compiling and running which will take around 45 minutes, take some time to look around the suite.

* How many nodes is the atmosphere running on?
* How many nodes is the ocean running on?

Changing the processor decomposition for the ocean is not as simple as just changing the EW/NS processes.  You also need to:

1. Recalculate the CICE number of columns per block EW and rows per block NS. (Normally the model is set up so that NEMO and CICE use the same decomposition). Looking at the current settings we calculate as follows:

  Num of cols per block EW = Num of cols EW / Num of processes EW (E.g. 360 / 9 = 40)

  Num of rows per block NS = Num of rows NS / Num of processes NS (E.g. 330 / 8 = 42) 

2. Recompile the ocean executable. Note the executable comprises both the ocean (NEMO) and sea-ice (CICE) code. 

Now looked at the ``coupled`` settings.   

* Can you see where the NEMO model settings appear? 

Look under *Run settings (namrun)*. The variables ``nn_stock`` and ``nn_write`` control the frequency of output files. 

* How often are NEMO restart files written? (Hint the NEMO timestep length is set as variable ``rn_rdt``).

Now browse the CICE settings.

* Can you find what the CICE restart frequency is set to? 

NEMO and CICE are developed separately from the UM, and you should have seen that they work in very different ways. See the websites for documentation: 

* http://oceans11.lanl.gov/trac/CICE 
* http://www.nemo-ocean.eu/

**iii. Output files**

**Log files** 

NEMO logging information is written to:

 ``~/cylc-run/<suitename>/work/<cycle>/coupled/ocean.output``

CICE logging information is written to: 

 ``~/cylc-run/<suitename>/work/<cycle>/coupled/ice_diag.d``

If the model fails some error messages may also be written to the file ``~/cylc-run/<suitename>/work/<cycle>/coupled/debug.root.01`` or ``debug.root.02``

When something goes wrong with the coupled model it can be tricky to work out what has gone wrong. NEMO errors may not appear at the end of the file but will be flagged with the string ``E R R O R``. 

**Restart files** 

Restart files go to the subdirectories ``NEMOhist`` and ``CICEhist`` in the standard data directory ``~/cylc-run/<suitename>/share/data/History_Data``.

**Diagnostic files**

Diagnostic files are left in the ``~/cylc-run/<suitename>/work/<cycle>/coupled/`` directory. 

CICE files start with ``<suitename>i``. Once your suite has run you should see the following CICE file: :: 

  archer$ ls ak943i*
  ak943i.10d.1978-09-10.nc

NEMO diagnostic files are named ``<suitename>o*grid_[TUVW]*``. To see what files are produced, run: :: 

  archer$ ls ak943o*grid*

In this case each processor writes to a separate file. To concatenate these into a global file use the ``rebuild_nemo`` tool, e.g.: :: 

  archer$ rebuild_nemo ak943o_10d_19780901_19780910_grid_W_19780901-19780910 72

Higher resolution NEMO suites may use the XIOS IO server. In this case, global files may be written directly, or each server process may write its own file. 
  
.. note:: The coupled atmos-ocean model setup is complex so we recommend you find a suite already setup for your needs.  If you find you do need to modify a coupled suite setup please contact NCAS-CMS for advice. 


