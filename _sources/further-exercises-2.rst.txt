Further Exercises (2)
=====================
   
The exercises in this section are all optional.  We suggest you pick and choose the exercises that you feel are most relevant to the work you are/will be doing.

.. note:: Use your copy of suite ``u-cc654`` for these exercises unless otherwise specified.

Post-Processing (archive and transfer of model data)
----------------------------------------------------

When your model runs it outputs data onto the ARCHER2 ``/work`` disk (``/projects`` on Monsoon2). If you are running a long integration and/or at high resolution data will mount up very quickly and you will need to move the data off of ARCHER2; for example to JASMIN.  The post-processing app (postproc) is used within cycling suites to automatically *archive*  model data and can be optionally configured to transfer the data from ARCHER2 to the JASMIN data facility.  The app archives and deletes model output files, not only for the UM, but also NEMO and CICE in coupled configurations.

Let's try configuring your suite to archive to a staging location on ARCHER2:

* Switch on post-processsing in window :guilabel:`suite conf --> Tasks`

The post-processing is configured under the :guilabel:`postproc` section:

* Select the :guilabel:`Archer` archiving system in window :guilabel:`Post Processing - common settings`.

A couple of new entries will have appeared in the index panel, :guilabel:`Archer Archiving` and :guilabel:`JASMIN Transfer`, identified with the blue dots.

You now need to specify where you want your archived data to be copied to:

* In the :guilabel:`Archer Archiving` panel set ``archive_root_dir`` to be ``/work/n02/n02/<userid>/archive``.  The ``archive_name`` (suite id) will be automatically appended to this.  

You will need to run the model for at least 1 day as archiving doesn't work for periods of less than 1 day.  Change the ``run length`` and ``cycling frequency`` to be 1 day.  This should complete in about 5 minutes so set the ``wallclock time`` to be 10 minutes. 

:guilabel:`Run` the suite.

Once the run has completed go to the archive directory for this cycle (e.g. ``/nerc/n02/n02/<userid>/<suiteid>/19880901T0000Z``) and you should see several files have been copied over (e.g ``cc654a.pc19880901_00.pp``).

Data files that have been archived and are no longer required by the model for restarting or for calculating means (seasonal, annual, etc) are deleted from the suite ``History_Data`` directory. Go to the ``History_Data`` directory for your suite and confirm that this has happened. This run is reinitialising the ``pc`` data stream every 6 hours and you should see that it has only removed data files for this stream up to 18:00hrs, the ``cc654a.pc19880901_18.pp`` file is still present.  This file contains data for the hours 18-24 and would be required by the model in order to restart. Equally seasonal mean files would not be fully archived until the end of the year, after the annual mean has been created.

.. note:: The post-processing app can also be configured to transfer the archived data over to JASMIN.  Details on how to do this are available on the CMS website: http://cms.ncas.ac.uk/wiki/Docs/PostProcessingApp

Using IO Servers
----------------

Older versions of the UM did not have IO servers, which meant that all reading and writing of fields files went through a single processor (pe0).  When the model is producing lots of data and is running on many processors, this method of IO is very inefficient and costly - when pe0 is writing data, all the other processors have to wait around doing nothing but still consuming AUs.  Later UM versions, including UM 10.5, have IO servers which are processors dedicated to performing IO and which work asynchronously with processors doing the computation.

Here's just a taste of how to get this working in your suite.

Set the suite to run for 1 day with an appropriate cycling frequency, then check that ``OpenMP`` is switched on as this is needed for the IO servers to work.

.. hint::
   Search for ``openmp`` in the rose edit GUI

Navigate to :guilabel:`suite conf --> Domain Decomposition --> Atmosphere` and check the number of ``OpenMP threads`` is set to ``2``. Set the number of ``IO Server Processes`` to ``8``.

:guilabel:`Save` and then :guilabel:`Run` the suite.

You will see lots of IO server log files in ``~/cylc-run/<suitename>/work/<cycle>/atmos_main`` which can be ignored for the most part.

Try repeating the :ref:`change_dump_freq` experiment with the IO servers switched on - you should see much faster performance.

Writing NetCDF output from the UM
---------------------------------

Until UM vn10.9, only fields-file output was available from the UM - bespoke NetCDF output configurations did exist but not on the UM trunk. The suite used in most of these Section 7 exercises is vn11.7, hence supports both fields-file and NetCDF output data formats.

Enable NetCDF
^^^^^^^^^^^^^
Make sure that ``IO Server Processes`` variable is set to ``0``.

Navigate to :guilabel:`um --> namelist --> Model Input and Output --> NetCDF Output Options` and set ``l_netcdf`` to ``true``. Several fields will appear which allow you to configure various NetCDF options.  For this exercise, leave them at their chosen values.

Set NetCDF Output Streams
^^^^^^^^^^^^^^^^^^^^^^^^^
Expand the :guilabel:`NetCDF Output Streams` section. A single stream - ``nc0`` - already exists; select it to display its content. As a useful comaprison, expand the :guilabel:`Model Output Streams` section and with the middle mouse button select :guilabel:`pp0`. Observe that the only significant differences between ``pp0`` and ``nc0`` are the values of ``file_id`` and ``filename_base``.  Data compression options for ``nc0`` are revealed if ``l_compress`` is set to ``true``. NetCDF deflation is a computationally expensive process best handled asynchronously to computation and as yet not fully implemented through the UM IO Server scheme (but under active development.) For many low- to medium-resolution models and, depending precisely on output profiles, high-resolution models also, use of UM-NetCDF without IO servers still provides significant benefits over fields-file output since using it avoids the need for subsequent file format conversion.

Right-click on :guilabel:`nc0` and select :guilabel:`Clone this section`. Edit the settings of the newly cloned section appropriately to make the new stream similar to ``pp1`` (ie. edit ``filename_base`` and all the reinitialisation variables). It is sensible to change the name of the new stream from ``1`` to something more meaningful, ``nc1`` for example (right click on ``1``, select :guilabel:`Rename a section`, and change ...nc(1) to ...nc (nc1)).

Direct output to the nc streams
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Expand :guilabel:`STASH Requests and Profiles`, then expand :guilabel:`Usage Profiles`. Assign nc streams to usage profiles - in this suite, UPA and UPB are assigned to ``pp0`` and ``pp1`` respectively (where can you see this?). Edit these Usage profiles to refer to ``nc0`` and ``nc1`` respectively. Run the STASH Macros (if you need a reminder see Section 6), save the changes, and run the suite. Check that the NetCDF output is what you expected.

Try adding more nc streams to mimic the pp stream behaviour.


Running the coupled model
-------------------------

The coupled model consists of the UM Atmosphere model coupled to the NEMO ocean and CICE sea ice models.  The coupled configuration used for this exercise is the UKESM Historical configuration with an N96 resolution for the atmosphere and a 1 degree ocean - you will see this written N96 ORCA1.

Checkout and run the suite
^^^^^^^^^^^^^^^^^^^^^^^^^^
Checkout and open the suite ``u-cs147``.  The first difference you should see is in the naming of the apps; there is a separate build app for the um and ocean, called ``fcm_make_um`` and ``fcm_make_ocean`` respectively. Similarly there are separate apps for the atmos and ocean model settings, called ``um`` and ``nemo_cice``.

Make the usual changes required to run the suite (i.e. set username, account code, queue). If you are following the tutorial as part of an organised training event, select one of the special queues, otherwise, select to run in the ``short`` queue.

Check that the suite is set to build the UM, Ocean, and Drivers as well as run the reconfiguration and model.

:guilabel:`Run` the suite.

Exploring the suite
^^^^^^^^^^^^^^^^^^^
Whilst the suite is compiling and running which will take around 40 minutes, take some time to look around the suite.

* How many nodes is the atmosphere running on?
* How many nodes is the ocean running on?
* What is the cycling frequency?

The version of NEMO used in this suite (and most suites you will come across) uses the XML IO Server (XIOS) to wite its diagnostic output. XIOS runs on dedicated nodes (one node in this case). Running ``squeue`` will show three status entries corresponding to the Atmosphere, Ocean, and XIOS components of the coupled suite. XIOS is running in ``multiple-file`` mode with 6 servers.

* Can you see where the NEMO model settings appear? 

Look under :guilabel:`Run settings (namrun)`. The variables ``nn_stock`` and ``nn_write`` control the frequency of output files.

* How often are NEMO restart files written?

.. hint:: The NEMO timestep length is set as variable ``rn_rdt``

Now browse the CICE settings.

* Can you find what the CICE restart frequency is set to? 

NEMO, CICE and XIOS are developed separately from the UM, and you should have seen that they work in very different ways. See the following websites for documentation: 

* http://oceans11.lanl.gov/trac/CICE 
* http://www.nemo-ocean.eu/
* https://forge.ipsl.jussieu.fr/ioserver

Output files
^^^^^^^^^^^^
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

CICE files start with ``<suitename>i``. Once your suite has run you should see the following CICE file (and more): :: 

  archer$ ls ce119i*
  ce119i.10d.1850-01-10.nc

NEMO diagnostic files are named ``<suitename>o*grid_[TUVW]*``. To see what files are produced, run: :: 

  archer$ ls ce119o*grid*

In this case each XIOS IO server writes to a separate file. To concatenate these into a global file use the ``rebuild_nemo`` tool, e.g.: :: 

  archer$ rebuild_nemo ce119o_1d_18500101_18500110_grid_T 6

.. note:: The coupled atmos-ocean model setup is complex so we recommend you find a suite already setup for your needs.  If you find you do need to modify a coupled suite setup please contact NCAS-CMS for advice. 

Running the Nesting Suite
-------------------------

The Nesting Suite drives a series of nested limited area models (LAM) from a global model.  It allows the user to specify the domains and it then automatically creates the required ancillary files and lateral boundary condition files.

Checkout and run the suite
^^^^^^^^^^^^^^^^^^^^^^^^^^
Checkout and open the suite ``u-ce122``.  There are a number of tasks for creating ancillary files (``ancil_*`` and ``ants_*``).  The global model set up is in :guilabel:`glm_um` and the LAMs are in :guilabel:`um`.  The task ``um-createbc`` creates the lateral boundary condition files.

Under :guilabel:`suite conf --> jinja2:suite.rc` are the main panels for controlling the Nesting Suite. Make the usual changes required to run the suite (i.e. set username, account code, queue).

If following the tutorial as part of an organised training event, select one of the special queues, otherwise, select the ``short`` queue.

:guilabel:`Run` the suite.

This particular suite has a global model and one limited area model. It should complete in about 45 - 60 minutes.

Exploring the Suite
^^^^^^^^^^^^^^^^^^^
The Driving Model set up panel allows the user to specify the resolution of the global model and the number of nested regions.

The :guilabel:`Nested Region 1` set up panel specifies the latitude and longitude of the centre of the first nested region.  All the other limited area models have the same centre.

A useful way to get this information is to use Google Maps.  Find the place you want as a centre and then press ``control-left mouse`` and a little window with the latitude and longitude appears.

 * Can you find out where the first LAM is located?

 .. hint:: Look at the orography file output during the ancillary creation.

The :guilabel:`resolution 1` set up panel specifies the grid and the run length.

The :guilabel:`Config 1` set up panel specifies the science configuration to be run.  Each LAM can have multiple science configurations.

Initial Data
^^^^^^^^^^^^
The initial data for the global model is in ``share/cycle/<cycle time>/glm/ics``

The initial data for the first LAM is in ``share/cycle/<cycle time>/Regn1/resn_1/RA1M/ics``

The RA1M is the name you gave to the first science configuration.

The LBCs for the first LAM are in ``share/cycle/<cycle time>/Regn1/resn_1/RA1M/lbcs``.

The ancillary files
^^^^^^^^^^^^^^^^^^^
These are in ``share/data/ancils/Regn1/resn_1``

The output files
^^^^^^^^^^^^^^^^
The global model output is in ``share/cycle/<cycle time>/glm/um``. This also contains contains the data for creating the LBC files (``umglaa_cb*``) for the first LAM.

Diagnostic files can be found under ``work/<cycle time>`` in an application directory.  For example, the region1 forecast diagnostics is in ``work/<cycle time>/Regn1_resn_1_RA1M_um_fcst_000``. This will include the pe_output files.

The output for the first LAM is in ``share/cycle/<cycle time>/Regn1/resn_1/RA1M/um``.

Further Information
^^^^^^^^^^^^^^^^^^^
This has been a very brief overview of the functionality of the Nesting Suite. The Nesting Suite is developed and maintained by Stuart Webster at the Met Office.  He has a web page all about the Nesting Suite at https://code.metoffice.gov.uk/trac/rmed/wiki/suites/nesting. This includes a more detailed tutorial.
